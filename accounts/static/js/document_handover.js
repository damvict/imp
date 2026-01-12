let selectedShipmentId = null;
let selectedAgentId = null;

document.addEventListener("DOMContentLoaded", fetchShipments);

async function fetchShipments() {
  const res = await fetch("/api/bank-controller-shipments/");
  const data = await res.json();

  const container = document.getElementById("shipments");
  container.innerHTML = "";

  if (data.length === 0) {
    container.innerHTML = `
      <div class="col-span-2 text-center text-green-600 font-semibold">
        All Documents Handed Over
      </div>`;
    return;
  }

  data.forEach(s => {
    container.innerHTML += `
      <div class="bg-white p-4 rounded shadow">
        <h3 class="font-bold">${s.shipment_code}</h3>
        <p class="text-gray-600">${s.supplier_name}</p>
        <p class="text-sm text-gray-400">BL: ${s.bl}</p>
        <p class="text-sm">Vessel: ${s.vessel}</p>
        <p class="text-sm">Value: $${s.amount}</p>

        <button onclick="openModal(${s.id})"
                class="mt-3 bg-blue-600 text-white px-4 py-2 rounded w-full">
          Record Handover
        </button>
      </div>
    `;
  });
}

async function openModal(shipmentId) {
  selectedShipmentId = shipmentId;
  selectedAgentId = null;
  document.getElementById("confirmBtn").disabled = true;

  document.getElementById("handoverModal").classList.remove("hidden");

  const res = await fetch("/api/clearing-agent-users/");
  const agents = await res.json();

  const list = document.getElementById("agents");
  list.innerHTML = "";

  agents.forEach(a => {
    list.innerHTML += `
      <div onclick="selectAgent(${a.id})"
           class="border p-2 rounded mb-2 cursor-pointer hover:bg-blue-50"
           id="agent-${a.id}">
        <div class="font-semibold">${a.display_name}</div>
        <div class="text-xs text-gray-500">${a.username}</div>
      </div>
    `;
  });
}

function selectAgent(agentId) {
  selectedAgentId = agentId;
  document.getElementById("confirmBtn").disabled = false;

  document.querySelectorAll("[id^='agent-']").forEach(el =>
    el.classList.remove("bg-blue-100", "border-blue-600")
  );

  document.getElementById(`agent-${agentId}`)
    .classList.add("bg-blue-100", "border-blue-600");
}

async function confirmHandover() {
  if (!selectedShipmentId || !selectedAgentId) return;

  const res = await fetch(`/api/confirm-handover/${selectedShipmentId}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRF(),
    },
    body: JSON.stringify({ clearing_agent_id: selectedAgentId }),
  });

  if (!res.ok) {
    alert("Failed to confirm handover");
    return;
  }

  closeModal();
  fetchShipments();
  alert("Handover confirmed successfully");
}

function closeModal() {
  document.getElementById("handoverModal").classList.add("hidden");
  selectedShipmentId = null;
  selectedAgentId = null;
}

function getCSRF() {
  return document.cookie
    .split("; ")
    .find(row => row.startsWith("csrftoken"))
    ?.split("=")[1];
}

document.getElementById("confirmBtn").onclick = confirmHandover;
