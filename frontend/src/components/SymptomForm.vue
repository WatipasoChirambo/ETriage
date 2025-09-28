<template>
  <div class="form-container">
    <h2>Hospital Triage Form</h2>

    <input v-model="phoneNumber" placeholder="Phone number" />
    <input v-model="firstName" placeholder="First name" />
    <input v-model="lastName" placeholder="Last name" />

    <label>Has Medical Scheme?</label>
    <select v-model="hasScheme">
      <option :value="false">No</option>
      <option :value="true">Yes</option>
    </select>

    <input v-if="hasScheme" v-model="medicalSchemeId" placeholder="Medical scheme ID" />
    <input v-if="hasScheme" v-model="memberNumber" placeholder="Member number" />

    <label>Symptoms:</label>
    <div v-for="symptom in symptomsList" :key="symptom.id" class="symptom-row">
      <input type="checkbox" :value="symptom.id" v-model="selectedSymptoms" />
      {{ symptom.name }}
      <input
        type="number"
        v-model.number="severityMap[symptom.id]"
        placeholder="Severity (1-5)"
        min="1"
        max="5"
      />
    </div>

    <button @click="submitSymptoms">Submit</button>

    <!-- <div v-if="response">
      <h3>Response:</h3>
      <pre class="text-black">{{ JSON.stringify(response, null, 2) }}</pre>
    </div> -->
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useToast } from 'vue-toastification'

const toast = useToast()

const phoneNumber = ref('')
const firstName = ref('')
const lastName = ref('')
const hasScheme = ref(false)
const medicalSchemeId = ref('')
const memberNumber = ref('')
const symptomsList = ref([])
const selectedSymptoms = ref([])
const severityMap = reactive({})
const response = ref(null)
const cases = ref([])

// Backend URL
const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

// Fetch symptoms on mount
onMounted(async () => {
  try {
    const res = await fetch(`${backendUrl}/symptoms/`)
    symptomsList.value = await res.json()
    symptomsList.value.forEach(s => (severityMap[s.id] = 1))
  } catch (err) {
    console.error('Failed to fetch symptoms:', err)
  }
})

// Submit form
const submitSymptoms = async () => {
  // Basic validation
  if (!phoneNumber.value) {
    toast.error('Phone number is required')
    return
  }
  if (selectedSymptoms.value.length === 0) {
    toast.error('Select at least one symptom')
    return
  }

  // Build severity array, default to 1 if undefined
  const severity = selectedSymptoms.value.map(id => {
    const s = severityMap[id]
    return s && s >= 1 ? s : 1
  })

  const payload = {
    phone_number: phoneNumber.value,
    first_name: firstName.value || null,
    last_name: lastName.value || null,
    has_scheme: hasScheme.value,
    medical_scheme_id: hasScheme.value ? medicalSchemeId.value || null : null,
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

    // Show nice toast with patient info
    toast.success(
      `Patient ${data.patient.first_name} ${data.patient.last_name} submitted successfully!\n` +
      `Triage Level: ${data.triage_case.triage_level}\n` +
      `Recommended Action: ${data.triage_case.recommended_action}`,
      { timeout: 8000 }
    )

    // Update admin dashboard live
    cases.value.push(data)

    // Clear form
    phoneNumber.value = ''
    firstName.value = ''
    lastName.value = ''
    hasScheme.value = false
    medicalSchemeId.value = ''
    memberNumber.value = ''
    selectedSymptoms.value = []
    Object.keys(severityMap).forEach(key => (severityMap[key] = 1))
  } catch (err) {
    response.value = { error: err.message }
    console.error(err.message)
    alert(`Error: ${err.message}`)
  }
}
</script>

<style scoped>
.form-container { max-width: 600px; margin: auto; font-family: Arial, sans-serif; }
input, select, button { width: 100%; margin: 5px 0; padding: 8px; }
button { cursor: pointer; background-color: #4CAF50; color: white; border: none; }
pre { background: #f3f3f3; padding: 10px; }
.symptom-row { display: flex; gap: 10px; align-items: center; margin-bottom: 5px; }
</style>