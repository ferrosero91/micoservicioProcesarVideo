# API Usage Examples

## Generate Technical Test

### Using curl (Bash/Linux/Mac)

```bash
curl -X POST http://localhost:9000/generate-technical-test \
  -H "Content-Type: application/json" \
  -d '{
    "profession": "Desarrollador Full Stack",
    "technologies": "React, Node.js, Express, MongoDB, TypeScript",
    "experience": "3 años desarrollando aplicaciones web escalables",
    "education": "Ingeniería de Sistemas"
  }'
```

### Using PowerShell (Windows)

```powershell
$body = @{
    profession = "Desarrollador Full Stack"
    technologies = "React, Node.js, Express, MongoDB, TypeScript"
    experience = "3 años desarrollando aplicaciones web escalables"
    education = "Ingeniería de Sistemas"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:9000/generate-technical-test" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### Using Python

```python
import requests

profile_data = {
    "profession": "Desarrollador Full Stack",
    "technologies": "React, Node.js, Express, MongoDB, TypeScript",
    "experience": "3 años desarrollando aplicaciones web escalables",
    "education": "Ingeniería de Sistemas"
}

response = requests.post(
    "http://localhost:9000/generate-technical-test",
    json=profile_data
)

result = response.json()
print(result["technical_test_markdown"])
```

### Using JavaScript/Node.js

```javascript
const axios = require('axios');

const profileData = {
  profession: "Desarrollador Full Stack",
  technologies: "React, Node.js, Express, MongoDB, TypeScript",
  experience: "3 años desarrollando aplicaciones web escalables",
  education: "Ingeniería de Sistemas"
};

axios.post('http://localhost:9000/generate-technical-test', profileData)
  .then(response => {
    console.log(response.data.technical_test_markdown);
  })
  .catch(error => {
    console.error('Error:', error.message);
  });
```

## Integration with Job Application

### Workflow Example

1. **Candidate uploads video** → API extracts profile
2. **Company reviews profile** → Selects candidate
3. **Company clicks "Generate Test"** → API creates technical test
4. **Test sent to candidate** → Candidate completes test
5. **Company evaluates** → Makes hiring decision

### Frontend Integration (React Example)

```jsx
import React, { useState } from 'react';

function GenerateTechnicalTest({ candidateProfile }) {
  const [loading, setLoading] = useState(false);
  const [test, setTest] = useState(null);

  const handleGenerateTest = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:9000/generate-technical-test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          profession: candidateProfile.profession,
          technologies: candidateProfile.technologies,
          experience: candidateProfile.experience,
          education: candidateProfile.education
        })
      });
      
      const data = await response.json();
      setTest(data.technical_test_markdown);
    } catch (error) {
      console.error('Error generating test:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <button onClick={handleGenerateTest} disabled={loading}>
        {loading ? 'Generando...' : 'Generar Prueba Técnica'}
      </button>
      
      {test && (
        <div className="markdown-content">
          {/* Render markdown content */}
          <ReactMarkdown>{test}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}
```

## Response Format

The API returns the technical test in Markdown format:

```json
{
  "technical_test_markdown": "# Prueba Técnica - Desarrollador Full Stack\n\n## Información General\n- Duración estimada: 2.5 horas\n...",
  "profile_summary": {
    "profession": "Desarrollador Full Stack",
    "technologies": "React, Node.js, Express, MongoDB, TypeScript",
    "experience": "3 años desarrollando aplicaciones web escalables"
  }
}
```

You can render the markdown using libraries like:
- **React:** `react-markdown`
- **Vue:** `vue-markdown`
- **Angular:** `ngx-markdown`
- **Plain JS:** `marked.js`
