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
            model: "llama3-8b-8192",
            messages: [
              { role: "system", content: "Eres un tutor de ruso experto para David Salazar. Enseña con fonética y ejemplos claros." },
              { role: "user", content: prompt }
            ]
          }),
        });
        const data = await response.json();
        return new Response(JSON.stringify({ response: data.choices[0].message.content }), {
          headers: { "Content-Type": "application/json" }
        });
      } catch (e) {
        return new Response(JSON.stringify({ response: "Error: " + e.message }), { 
          status: 500,
          headers: { "Content-Type": "application/json" }
        });
      }
    }
    return env.ASSETS.fetch(request);
  },
};
