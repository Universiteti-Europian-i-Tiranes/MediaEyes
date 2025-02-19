const countrySelect = document.getElementById("country");
const countryLabel = document.getElementById("country-label");

const countryNames = {
  us: "United States",
  uk: "United Kingdom",
  al: "Albania",
  in: "India",
  au: "Australia",
  ca: "Canada"
  // Add more countries here
};

countrySelect.addEventListener("change", () => {
  const selectedCountry = countrySelect.value;
  countryLabel.textContent = countryNames[selectedCountry] 
    ? `from ${countryNames[selectedCountry]}` 
    : "";
});