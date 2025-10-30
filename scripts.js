document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.tab-button');
    
    const formRefugiado = document.getElementById('form-refugiado');
    const formVoluntario = document.getElementById('form-voluntario');

    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            tabButtons.forEach(btn => btn.classList.remove('active'));
      
            this.classList.add('active');

          
            const formToShow = this.getAttribute('data-form');

            
            if (formToShow === 'refugiado') {
             
                formRefugiado.classList.remove('hidden');
                formVoluntario.classList.add('hidden');
            } else if (formToShow === 'voluntario') {
                
                formVoluntario.classList.remove('hidden');
                formRefugiado.classList.add('hidden');
            }
        });
    });

    
    formRefugiado.addEventListener('submit', function(e) {
        e.preventDefault(); 
        alert('Formulário de Refugiado submetido! (Apenas simulação)');
     
    });

    formVoluntario.addEventListener('submit', function(e) {
        e.preventDefault(); 
        alert('Formulário de Voluntário submetido! (Apenas simulação)');
        
    });
});