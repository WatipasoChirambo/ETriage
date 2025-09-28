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
      <input type="number" v-model.number="severityMap[symptom.id]" placeholder="Severity" min="1" max="5" />
    </div>

    <button @click="submitSymptoms">Submit</button>

    <div v-if="response">
      <h3>Response:</h3>
      <pre>{{ JSON.stringify(response, null, 2) }}</pre>
    </div>

    <div v-if="cases.length">
      <h3>Admin Dashboard (Live)</h3>
      <table border="1" cellpadding="5">
        <tr>
          <th>Patient</th>
          <th>Phone</th>
          <th>Symptoms</th>
          <th>Severity</th>
          <th>Triage Level</th>
          <th>Action</th>
        </tr>
        <tr v-for="c in cases" :key="c.id">
          <td>{{ c.first_name }} {{ c.last_name }}</td>
          <td>{{ c.phone_number }}</td>
          <td>{{ c.symptoms.map(s => s.symptom_id).join(', ') }}</td>
          <td>{{ c.symptoms.map(s => s.severity).join(', ') }}</td>
          <td>{{ c.triage_case.triage_level }}</td>
          <td>{{ c.triage_case.recommended_action }}</td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

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

// Backend URL (Docker network or localhost)
const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

// Fetch symptom list on mount
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
  const payload = {
    phone_number: phoneNumber.value,
    first_name: firstName.value,
    last_name: lastName.value,
    has_scheme: hasScheme.value,
    medical_scheme_id: hasScheme.value ? medicalSchemeId.value : null,
    member_number: hasScheme.value ? memberNumber.value : null,
    symptoms: selectedSymptoms.value,
    severity: selectedSymptoms.value.map(id => severityMap[id])
  }

  try {
    const res = await fetch(`${backendUrl}/submit_symptoms/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    const data = await res.json()
    response.value = data

    // Update admin dashboard live
    cases.value.push(data)
    
    // Clear form after submission
    phoneNumber.value = ''
    firstName.value = ''
    lastName.value = ''
    hasScheme.value = false
    medicalSchemeId.value = ''
    memberNumber.value = ''
    selectedSymptoms.value = []
  } catch (err) {
    response.value = { error: err.message }
    console.log(err.message)
  }
}
</script>

<style scoped>
.form-container { max-width: 600px; margin: auto; font-family: Arial, sans-serif; }
input, select, button { width: 100%; margin: 5px 0; padding: 8px; }
button { cursor: pointer; background-color: #4CAF50; color: white; border: none; }
pre { background: #f3f3f3; padding: 10px; }
.symptom-row { display: flex; gap: 10px; align-items: center; margin-bottom: 5px; }
table { width: 100%; margin-top: 20px; border-collapse: collapse; }
th, td { padding: 8px; text-align: left; }
</style>
