<template>
  <div class="enterprise-wrapper">
    <div class="enterprise-container">
      <!-- Header -->
      <header class="enterprise-header">
        <h1 class="title">Welcome to Capsule</h1>
        <p class="subtitle">Quick & secure check-in</p>
      </header>

      <!-- Form Steps -->
      <transition name="fade-slide" mode="out-in">
        <!-- Step 1: Personal Info -->
        <div v-if="step === 1" key="step1" class="step-card">
          <h2 class="step-title">Patient Information</h2>
          <input v-model="phoneNumber" placeholder="Phone number" type="tel" />
          <input v-model="firstName" placeholder="First name" />
          <input v-model="lastName" placeholder="Last name" />
          <button @click="nextStep" class="btn btn-primary">Next</button>
        </div>

        <!-- Step 2: Hospital Selection -->
        <div v-else-if="step === 2" key="step2" class="step-card">
          <h2 class="step-title">Hospital Selection</h2>
          <select v-model="selectedHospital" aria-label="Select Hospital">
            <option disabled value="">-- Select Hospital --</option>
            <option v-for="hospital in hospitals" :key="hospital.id" :value="hospital.id">
              {{ hospital.name }}
            </option>
          </select>
          <div class="btn-row">
            <button @click="prevStep" class="btn btn-secondary">Back</button>
            <button @click="nextStep" class="btn btn-primary">Next</button>
          </div>
        </div>

        <!-- Step 3: Medical Scheme -->
        <div v-else-if="step === 3" key="step3" class="step-card">
          <h2 class="step-title">Medical Scheme</h2>
          <select v-model="hasScheme" aria-label="Do you have a medical scheme?">
            <option :value="false">No</option>
            <option :value="true">Yes</option>
          </select>

          <div v-if="hasScheme" class="scheme-details">
            <select v-model.number="medicalSchemeId" aria-label="Select Medical Scheme">
              <option disabled value="">-- Select Scheme --</option>
              <option v-for="scheme in medicalSchemes" :key="scheme.id" :value="scheme.id">
                {{ scheme.name }}
              </option>
            </select>
            <input v-model="memberNumber" placeholder="Membership number" />
          </div>

          <div class="btn-row">
            <button @click="prevStep" class="btn btn-secondary">Back</button>
            <button @click="nextStep" class="btn btn-primary">Next</button>
          </div>
        </div>

        <!-- Step 4: Symptoms -->
        <div v-else-if="step === 4" key="step4" class="step-card">
          <h2 class="step-title">Symptoms Assessment</h2>
          <div v-for="symptom in symptomsList" :key="symptom.id" class="symptom-card">
            <label class="checkbox-wrapper">
              <input type="checkbox" :value="symptom.id" v-model="selectedSymptoms" />
              <span class="checkmark"></span>
              {{ symptom.name }}
            </label>
            <input
              type="number"
              v-model.number="severityMap[symptom.id]"
              placeholder="1-5"
              min="1"
              max="5"
              :disabled="!selectedSymptoms.includes(symptom.id)"
              class="severity-input"
            />
          </div>

          <button @click="submitSymptoms" class="btn btn-success submit-btn">Submit</button>
        </div>
      </transition>
    </div>
  </div>
</template>

<style scoped>
/* ----------------- Layout ----------------- */
.enterprise-wrapper {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f3f6fa;
  padding: 20px;
  box-sizing: border-box;
}

.enterprise-container {
  width: 100%;
  max-width: 650px;
  background: #ffffff;
  border-radius: 20px;
  padding: 40px 35px;
  box-shadow: 0 15px 40px rgba(0,0,0,0.08);
}

/* ----------------- Header ----------------- */
.enterprise-header {
  text-align: center;
  margin-bottom: 30px;
}

.title {
  font-size: 2.2rem;
  font-weight: 700;
  color: #1b2733;
}

.subtitle {
  font-size: 1.1rem;
  color: #555;
}

/* ----------------- Step Card ----------------- */
.step-card {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.step-title {
  font-size: 1.4rem;
  font-weight: 600;
  color: #1b2733;
  margin-bottom: 15px;
}

/* ----------------- Inputs ----------------- */
input,
select {
  width: 100%;
  padding: 15px;
  border-radius: 12px;
  border: 1px solid #ccc;
  font-size: 1rem;
  outline: none;
  transition: 0.3s;
}
input:focus,
select:focus {
  border-color: #4caf50;
  box-shadow: 0 0 12px rgba(76,175,80,0.2);
}

/* ----------------- Buttons ----------------- */
.btn {
  padding: 15px;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  transition: 0.3s;
}
.btn-primary { background: #4caf50; color: #fff; }
.btn-primary:hover { background: #45a049; }
.btn-secondary { background: #e0e0e0; color: #333; }
.btn-secondary:hover { background: #d5d5d5; }
.btn-success { background: #2196f3; color: #fff; }
.btn-success:hover { background: #1976d2; }

.btn-row {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

/* ----------------- Symptoms ----------------- */
.symptom-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f1f9ff;
  padding: 12px 20px;
  border-radius: 15px;
  margin-bottom: 10px;
  transition: transform 0.2s, box-shadow 0.2s;
}
.symptom-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(0,0,0,0.1);
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 500;
  user-select: none;
  position: relative;
  cursor: pointer;
}

.checkbox-wrapper input {
  opacity: 0;
  width: 0;
  height: 0;
}

.checkmark {
  width: 22px;
  height: 22px;
  border: 2px solid #4caf50;
  border-radius: 50%;
  display: inline-block;
  position: relative;
  transition: all 0.2s;
}
.checkbox-wrapper input:checked + .checkmark {
  background-color: #4caf50;
}
.checkmark::after {
  content: "";
  position: absolute;
  display: none;
}
.checkbox-wrapper input:checked + .checkmark::after {
  display: block;
  left: 7px;
  top: 3px;
  width: 5px;
  height: 11px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.severity-input {
  width: 60px;
  text-align: center;
  border-radius: 10px;
  border: 1px solid #4caf50;
  outline: none;
  transition: 0.2s;
}
.severity-input:disabled {
  background: #f5f5f5;
  border-color: #ccc;
}

/* ----------------- Animations ----------------- */
.fade-slide-enter-active, .fade-slide-leave-active {
  transition: all 0.5s ease;
}
.fade-slide-enter-from { opacity: 0; transform: translateY(20px); }
.fade-slide-enter-to { opacity: 1; transform: translateY(0); }
.fade-slide-leave-from { opacity: 1; transform: translateY(0); }
.fade-slide-leave-to { opacity: 0; transform: translateY(-20px); }

/* ----------------- Responsive ----------------- */
@media (max-width: 700px) {
  .enterprise-container {
    padding: 30px 20px;
  }
  .title { font-size: 1.8rem; }
  .step-title { font-size: 1.2rem; }
  input, select, .btn { font-size: 0.95rem; }
}
</style>


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
    console.log(err)
    toast.error(`Error: ${err.message}`)
  }
}
</script>