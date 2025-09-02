document.getElementById("ai-summary").addEventListener("change", async function() {
    if (this.checked) {
        const summary = document.getElementById("summary").value;
        const resp = await fetch("/ai/summary", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ summary: summary })
        });
        const data = await resp.json();
        document.getElementById("summary").value = data.enhanced;
    }
});
