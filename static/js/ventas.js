// Script para autocompletar precio unitario cuando se selecciona un producto
document.addEventListener('DOMContentLoaded', function() {
    const selectElements = document.querySelectorAll('select[id*="producto"]');
    
    selectElements.forEach(select => {
        // Almacenar datos de productos
        const productData = {};
        Array.from(select.options).forEach(option => {
            if (option.value) {
                productData[option.value] = {
                    text: option.text,
                    precio: option.getAttribute('data-precio'),
                    cantidad: option.getAttribute('data-cantidad')
                };
            }
        });
        
        select.addEventListener('change', function() {
            const row = this.closest('tr');
            if (!row) return;
            
            const selectedValue = this.value;
            const precioInput = row.querySelector('input[id*="precio_unitario"]');
            
            if (selectedValue && productData[selectedValue]) {
                const precio = productData[selectedValue].precio;
                if (precioInput && precio) {
                    precioInput.value = parseFloat(precio).toFixed(2);
                }
            }
        });
    });
});
