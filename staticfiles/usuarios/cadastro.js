// usuarios/static/usuarios/js/cadastro.js

document.addEventListener('DOMContentLoaded', function() {
    
    // 0. REFERÊNCIAS DOS ELEMENTOS
    const tabButtons = document.querySelectorAll('.tab-button');
    const dataNascInput = document.getElementById('data-nasc');
    const telRefugiadoInput = document.getElementById('telefone-refugiado');
    const telVoluntarioInput = document.getElementById('telefone-voluntario');
    const cepInput = document.getElementById('cep-refugiado');
    const logradouroInput = document.getElementById('logradouro');
    const bairroInput = document.getElementById('bairro');
    const cidadeInput = document.getElementById('cidade-refugiado');
    const estadoInput = document.getElementById('estado-refugiado');
    
    // --- 1. LÓGICA DE TROCA DE ABAS (Para garantir que a tela apareça) ---
    
    if (tabButtons.length) {
        document.querySelectorAll('.formulario.hidden').forEach(form => form.classList.add('hidden')); // Esconde todos por padrão

        tabButtons.forEach(button => {
            button.addEventListener('click', function() {
                const formId = this.getAttribute('data-form');
                document.querySelectorAll('.formulario').forEach(f => f.classList.add('hidden'));
                document.getElementById(`form-${formId}`).classList.remove('hidden');

                tabButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
            });
        });
    }

    // --- 2. FUNÇÕES DE MÁSCARA ---
    
    // Data: dd/mm/yyyy
    const maskDate = (value) => {
        value = value.replace(/\D/g, ""); 
        value = value.replace(/^(\d{2})(\d)/, "$1/$2");
        value = value.replace(/^(\d{2})\/(\d{2})(\d)/, "$1/$2/$3"); 
        return value.substring(0, 10);
    };

    // Telefone: (00) 00000-0000
    const maskPhone = (value) => {
        value = value.replace(/\D/g, "");
        value = value.replace(/^(\d{2})(\d)/g, "($1) $2");
        value = value.replace(/(\d)(\d{4})$/, "$1-$2");
        return value.substring(0, 15);
    };
    
    // CEP: 00000-000
    const maskCEP = (value) => {
        value = value.replace(/\D/g, "");
        value = value.replace(/^(\d{5})(\d)/, "$1-$2");
        return value.substring(0, 9);
    };
    
    // --- 3. APLICAR MÁSCARAS AOS INPUTS ---
    
    // Data de Nascimento
    if (dataNascInput) dataNascInput.addEventListener('input', (e) => { e.target.value = maskDate(e.target.value); });
    // Telefones
    if (telRefugiadoInput) telRefugiadoInput.addEventListener('input', (e) => { e.target.value = maskPhone(e.target.value); });
    if (telVoluntarioInput) telVoluntarioInput.addEventListener('input', (e) => { e.target.value = maskPhone(e.target.value); });
    // CEP
    if (cepInput) cepInput.addEventListener('input', (e) => { e.target.value = maskCEP(e.target.value); });
    
    // --- 4. LÓGICA DE CONSULTA DE CEP (ViaCEP) ---
    
    function clearAddressFields() {
        if(logradouroInput) logradouroInput.value = '';
        if(bairroInput) bairroInput.value = '';
        if(cidadeInput) cidadeInput.value = '';
        if(estadoInput) estadoInput.value = 'UF';
    }

    if (cepInput && logradouroInput) {
        cepInput.addEventListener('blur', function() {
            let cep = cepInput.value.replace(/\D/g, '');

            if (cep.length === 8) {
                clearAddressFields();
                
                fetch(`https://viacep.com.br/ws/${cep}/json/`)
                    .then(response => response.json())
                    .then(data => {
                        if (!data.erro) {
                            if(logradouroInput) logradouroInput.value = data.logradouro || '';
                            if(bairroInput) bairroInput.value = data.bairro || '';
                            if(cidadeInput) cidadeInput.value = data.localidade || '';
                            if(estadoInput) estadoInput.value = data.uf || 'UF';
                            // Foca no campo número (ID para o campo que você chamou de 'numero-endereco')
                            const numInput = document.getElementById('numero-endereco');
                            if (numInput) numInput.focus();
                        } else {
                            alert("CEP não encontrado.");
                            clearAddressFields();
                        }
                    })
                    .catch(() => {
                        alert("Erro na consulta do CEP.");
                        clearAddressFields();
                    });
            } else if (cep.length > 0) {
                clearAddressFields();
            }
        });
    }
});