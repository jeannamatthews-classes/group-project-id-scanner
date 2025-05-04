const modal = document.getElementById('waiverModal');
const openBtn = document.getElementById('openWaiverBtn');
const closeBtn = document.getElementById('closeModalBtn');
const agreeBtn = document.getElementById('agreeBtn');
const agreeCheckbox = document.getElementById('agreeCheckbox');
const form = document.querySelector('form');

let waiverSigned = false;

openBtn.onclick = () => {
  modal.style.display = "block";
};

closeBtn.onclick = () => {
  modal.style.display = "none";
};

agreeBtn.onclick = () => {
  if (agreeCheckbox.checked) {
    waiverSigned = true;
    modal.style.display = "none";
  } else {
    alert("Please check the box to agree to the waiver terms.");
  }
};

form.onsubmit = (e) => {
  if (!waiverSigned) {
    e.preventDefault();
    alert("You must sign the waiver before registering.");
  }
};
