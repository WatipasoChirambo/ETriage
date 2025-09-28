<template>
  <div class="form-container">
    <h2>Hospital Triage Form</h2>

    <!-- Step 1: Personal Info -->
    <div v-if="step === 1">
      <input v-model="phoneNumber" placeholder="Phone number" />
      <input v-model="firstName" placeholder="First name" />
      <input v-model="lastName" placeholder="Last name" />
      <button @click="nextStep">Next</button>
    </div>

    <!-- Step 2: Select Hospital -->
    <div v-if="step === 2">
      <label>Select Hospital:</label>
      <select v-model="selectedHospital">
        <option disabled value="">-- Select Hospital --</option>
        <option v-for="hospital in hospitals" :key="hospital.id" :value="hospital.id">
          {{ hospital.name }}
        </option>
      </select>
      <button @click="prevStep">Back</button>
      <button @click="nextStep">Next</button>
    </div>

    <!-- Step 3: Medical Scheme -->
    <div v-if="step === 3">
      <label>Has Medical Scheme?</label>
      <select v-model="hasScheme">
        <option :value="false">No</option>
        <option :value="true">Yes</option>
      </select>

      <div v-if="hasScheme">
        <label>Select Medical Scheme:</label>
        <select v-model.number="medicalSchemeId">
          <option disabled value="">-- Select Scheme --</option>
          <option v-for="scheme in medicalSchemes" :key="scheme.id" :value="scheme.id">
            {{ scheme.name }}
          </option>
        </select>

        <input v-model="memberNumber" placeholder="Member number" />
      </div>

      <button @click="prevStep">Back</button>
      <button @click="nextStep">Next</button>
    </div>

    <!-- Step 4: Symptoms -->
    <div v-if="step === 4">
      <label>Symptoms:</label>
      <div v-for="symptom in symptomsList" :key="symptom.id" class="symptom-row">
        <input
          type="checkbox"
          :value="symptom.id"
          v-model="selectedSymptoms"
        />
        {{ symptom.name }}
        <input
          type="number"
          v-model.number="severityMap[symptom.id]"
          placeholder="Severity (1-5)"
          min="1"
          max="5"
          :disabled="!selectedSymptoms.includes(symptom.id)"
        />
      </div>

      <button @click="prevStep">Back</button>
      <button @click="submitSymptoms">Submit</button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
const toast = useToast()

// Step control
const step = ref(1)

// Form fields
const phoneNumber = ref('')
const firstName = ref('')
const lastName = ref('')
const selectedHospital = ref('')
const hasScheme = ref(false)
const medicalSchemeId = ref('')
const memberNumber = ref('')
const symptomsList = ref([])
const selectedSymptoms = ref([])
const severityMap = reactive({})
const response = ref(null)
const cases = ref([])

// Data from backend
const hospitals = ref([])
const medicalSchemes = ref([])

// Backend URL
const backendUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Fetch hospitals, symptoms, and schemes on mount
onMounted(async () => {
  try {
    const [hospitalRes, symptomsRes, schemeRes] = await Promise.all([
      fetch(`${backendUrl}/hospitals/`),
      fetch(`${backendUrl}/symptoms/`),
      fetch(`${backendUrl}/medical_schemes/`),
    ])

    hospitals.value = await hospitalRes.json()
    symptomsList.value = await symptomsRes.json()
    symptomsList.value.forEach(s => (severityMap[s.id] = 1))
    medicalSchemes.value = await schemeRes.json()
  } catch (err) {
    console.error('Failed to fetch data:', err)
    toast.error('Failed to load hospitals, symptoms, or schemes')
  }
})

// Step navigation
const nextStep = () => {
  if (step.value === 1 && !phoneNumber.value) {
    toast.error('Phone number is required')
    return
  }
  if (step.value === 2 && !selectedHospital.value) {
    toast.error('Please select a hospital')
    return
  }
  if (step.value === 3 && hasScheme.value && !medicalSchemeId.value) {
    toast.error('Please select a medical scheme')
    return
  }
  step.value++
}

const prevStep = () => {
  if (step.value > 1) step.value--
}

// Submit form
const submitSymptoms = async () => {
  if (selectedSymptoms.value.length === 0) {
    toast.error('Select at least one symptom')
    return
  }

  const severity = selectedSymptoms.value.map(id => severityMap[id] || 1)
  const payload = {
    phone_number: phoneNumber.value,
    first_name: firstName.value || null,
    last_name: lastName.value || null,
    hospital_id: parseInt(selectedHospital.value),
    has_scheme: hasScheme.value,
    medical_scheme_id: hasScheme.value ? parseInt(medicalSchemeId.value) || null : null,
    member_number: hasScheme.value ? memberNumber.value || null : null,
    symptoms: selectedSymptoms.value,
    severity
  }

  try {
    const res = await fetch(`${backendUrl}/submit_symptoms/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (!res.ok) {
      const errText = await res.text()
      console.error('Backend error:', errText)
      toast.error('Server error occurred')
      return
    }

    const data = await res.json()
    response.value = data
    cases.value.push(data)

    toast.success(
      `Patient ${data.patient.first_name} ${data.patient.last_name} submitted successfully!\n` +
      `Triage Level: ${data.triage_case.triage_level}\n` +
      `Recommended Action: ${data.triage_case.recommended_action}`,
      { timeout: 8000 }
    )

    // Reset form
    step.value = 1
    phoneNumber.value = ''
    firstName.value = ''
    lastName.value = ''
    selectedHospital.value = ''
    hasScheme.value = false
    medicalSchemeId.value = ''
    memberNumber.value = ''
    selectedSymptoms.value = []
    Object.keys(severityMap).forEach(key => (severityMap[key] = 1))
  } catch (err) {
    console.error(err)
    toast.error(`Error: ${err.message}`)
  }
}
</script>

<style scoped>
.form-container {
  max-width: 600px;
  margin: auto;
  font-family: Arial, sans-serif;
}
input,
select,
button {
  width: 100%;
  margin: 5px 0;
  padding: 8px;
}
button {
  cursor: pointer;
  background-color: #4caf50;
  color: white;
  border: none;
}
.symptom-row {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 5px;
}
</style>
