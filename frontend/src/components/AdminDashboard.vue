<template>
  <div>
    <h2>Admin Dashboard</h2>
    <div v-if="cases.length === 0">No triage cases yet.</div>
    <table v-else border="1" cellpadding="5">
      <tr>
        <th>Patient</th>
        <th>Phone</th>
        <th>Symptoms</th>
        <th>Severity</th>
        <th>Triage Level</th>
        <th>Recommended Action</th>
      </tr>
      <tr v-for="c in cases" :key="c.patient.id">
        <td>{{ c.patient.first_name }} {{ c.patient.last_name }}</td>
        <td>{{ c.patient.phone_number }}</td>
        <td>{{ c.patient.symptoms.map(s => getSymptomName(s.symptom_id)).join(', ') }}</td>
        <td>{{ c.patient.symptoms.map(s => s.severity).join(', ') }}</td>
        <td :style="{ color: getTriageColor(c.triage_case.triage_level) }">{{ c.triage_case.triage_level }}</td>
        <td>{{ c.triage_case.recommended_action }}</td>
      </tr>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const cases = ref([])
const symptomsList = ref([])  // to map IDs to names
const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

// Fetch symptoms for ID->name mapping
onMounted(async () => {
  try {
    const resSym = await fetch(`${backendUrl}/symptoms/`)
    symptomsList.value = await resSym.json()

    const resCases = await fetch(`${backendUrl}/triage_cases/`)
    cases.value = await resCases.json()
  } catch (err) {
    console.error('Failed to fetch data:', err)
  }
})

const getSymptomName = (id) => {
  const s = symptomsList.value.find(sym => sym.id === id)
  return s ? s.name : id
}

const getTriageColor = (level) => {
  switch (level) {
    case 'high': return 'red'
    case 'medium': return 'orange'
    case 'low': return 'green'
    default: return 'black'
  }
}
</script>

<style scoped>
table { width: 100%; margin-top: 20px; border-collapse: collapse; }
th, td { padding: 8px; text-align: left; }
</style>
