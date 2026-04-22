export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/chat" && request.method === "POST") {
      try {
        const { prompt } = await request.json();
        const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${env.GROQ_API_KEY}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            model: "llama-3.3-70b-versatile",
            messages: [
              { role: "system", content: "Eres un tutor de ruso experto para David Salazar. Responde con texto plano. PROHIBIDO usar asteriscos, negritas o símbolos Markdown. Solo texto limpio." },
              { role: "user", content: prompt }
            ]
          }),
        });
        const data = await response.json();
        if (data.choices && data.choices.length > 0) {
          return new Response(JSON.stringify({ response: data.choices[0].message.content }), {
            headers: { "Content-Type": "application/json" }
          });
        }
        return new Response(JSON.stringify({ response: "Error de API" }), { headers: { "Content-Type": "application/json" } });
      } catch (e) {
        return new Response(JSON.stringify({ response: "Error" }), { headers: { "Content-Type": "application/json" } });
      }
    }
    return env.ASSETS.fetch(request);
  },
};
