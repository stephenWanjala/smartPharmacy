document.addEventListener("DOMContentLoaded", function () {
    const quantityInput = document.getElementById('quantity-sold');
    const sellingPriceInput = document.getElementById('selling-price');

    quantityInput.addEventListener('input', function () {
        const quantity = parseInt(quantityInput.value) || 0; // Ensure a valid integer

        // Get the medicine's selling price from the form data
        const medicineSellingPrice = parseFloat(document.querySelector(`option[value='${quantityInput.value}']`).dataset.sellingPrice);

        // Calculate the total selling price and update the input field
        const totalSellingPrice = quantity * medicineSellingPrice;
        sellingPriceInput.value = totalSellingPrice.toFixed(2);
    });
});
