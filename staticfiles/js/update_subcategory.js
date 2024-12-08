document.addEventListener("DOMContentLoaded", function() {
    const categoryField = document.querySelector("#id_category");
    const subCategoryField = document.querySelector("#id_sub_category");
    const unitField = document.querySelector("#id_unit");

    if (!categoryField || !subCategoryField || !unitField) {
        console.log("Required elements are missing from the DOM.");
        return;
    }

    const subCategories = {
        'Transport': [['Car', 'Car'], ['Bus', 'Bus'], ['Train', 'Train']],
        'Buildings': [['Electricity', 'Electricity'], ['Heating', 'Heating']],
        'Industry': [['Manufacturing', 'Manufacturing'], ['Construction', 'Construction']],
    };

    const units = {
        'Car': 'KM',
        'Bus': 'KM',
        'Train': 'KM',
        'Electricity': 'KWH',
        'Heating': 'KWH',
        'Manufacturing': 'Units',
        'Construction': 'Hours',
    };

    function updateSubCategories() {
        const selectedCategory = categoryField.value;
        const options = subCategories[selectedCategory] || [];
        
        subCategoryField.innerHTML = '';

        options.forEach(option => {
            const newOption = document.createElement("option");
            newOption.value = option[0];
            newOption.textContent = option[1];
            subCategoryField.appendChild(newOption);
        });

        updateUnit();
    }

    function updateUnit() {
        const selectedSubCategory = subCategoryField.value;
        const unit = units[selectedSubCategory] || '';
        unitField.value = unit; 
    }

    categoryField.addEventListener("change", updateSubCategories);
    subCategoryField.addEventListener("change", updateUnit);

    updateSubCategories();
});
