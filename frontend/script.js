const API = "http://127.0.0.1:5000";

function addProduct() {
    const pid = document.getElementById("productId").value.trim();
    const pname = document.getElementById("productName").value.trim();
    const loc = document.getElementById("location").value.trim();
    const message = document.getElementById("message");

    if (!pid || !pname || !loc) {
        message.innerText = "❌ Please fill all fields";
        return;
    }

    fetch("http://127.0.0.1:5000/add-product", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            product_id: pid,
            product_name: pname,
            location: loc
        })
    })
    .then(res => res.json())
    .then(data => {
        message.innerText = data.status || data.error;
    })
    .catch(() => {
        message.innerText = "❌ Backend not running";
    });
}


function updateLocation() {
    const pid = updateId.value.trim();
    const loc = newLocation.value.trim();

    if (!pid || !loc) {
        message.innerText = "❌ Please fill all fields";
        return;
    }

    fetch(`${API}/update-location`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            product_id: pid,
            location: loc
        })
    })
    .then(res => res.json())
    .then(data => {
        message.innerText = data.status || data.error;
    });
}

function trackProduct() {
    const pid = trackId.value.trim();
    const timeline = document.getElementById("timeline");
    timeline.innerHTML = "";

    if (!pid) {
        timeline.innerText = "❌ Enter Product ID";
        return;
    }

    fetch(`${API}/track/${pid}`)
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            timeline.innerText = data.error;
            return;
        }

        data.history.forEach((block, i) => {
            timeline.innerHTML += `
                <div class="timeline-item">
                    <div class="dot"></div>
                    <div class="content">
                        <h3>Step ${i + 1}</h3>
                        <p><b>Location:</b> ${block.location}</p>
                        <p><b>Time:</b> ${block.time}</p>
                        <p class="hash"><b>Hash:</b> ${block.hash}</p>
                        <p class="hash"><b>Prev:</b> ${block.previous_hash}</p>
                    </div>
                </div>
            `;
        });
    });
}

function verifyBlockchain() {
    const pid = trackId.value.trim();
    const result = document.getElementById("verifyResult");

    if (!pid) {
        result.innerText = "❌ Enter Product ID first";
        return;
    }

    fetch(`http://127.0.0.1:5000/verify/${pid}`)
    .then(res => res.json())
    .then(data => {
        if (data.status.includes("VERIFIED")) {
            result.innerText = `✅ Blockchain Verified (${data.blocks} blocks)`;
            result.style.color = "#00ffcc";
        } else {
            result.innerText = `❌ Blockchain Tampered at Block ${data.block}`;
            result.style.color = "#ff4c4c";
        }
    });
}
