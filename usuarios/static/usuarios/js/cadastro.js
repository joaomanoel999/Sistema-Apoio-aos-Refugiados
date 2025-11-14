// O código é executado somente após o carregamento completo do DOM
$(document).ready(function() {
    
    // =============================================================
    // A. MÁSCARAS DE INPUT (jQuery Mask Plugin) - MANTIDAS
    // =============================================================

    // 1. Data de Nascimento: DD/MM/AAAA
    $('.data-nascimento').mask('00/00/0000', {placeholder: "DD/MM/AAAA"});

    // 2. Telefone: (XX) XXXXX-XXXX ou (XX) XXXX-XXXX (máscara dinâmica)
    var phoneMaskBehavior = function (val) {
      return val.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00009';
    },
    options = {
      onKeyPress: function(val, e, field, options) {
          field.mask(phoneMaskBehavior.apply({}, arguments), options);
      }
    };
    
    $('.telefone').mask(phoneMaskBehavior, options);
    
    // 3. Máscara de CEP
    $('.cep-input').mask('00000-000');


    // =============================================================
    // B. LÓGICA DE TROCA DE ABAS - MANTIDA
    // =============================================================
    
    $('.tab-button').on('click', function() {
        $('.tab-button').removeClass('active');
        $(this).addClass('active');

        var targetFormId = $(this).data('target');

        $('.registration-form').removeClass('active').addClass('hidden');
        $('#' + targetFormId).removeClass('hidden').addClass('active');
    });

    // =============================================================
    // C. INTEGRAÇÃO VIACEP - AJUSTADA
    // =============================================================

    // Função que limpa os campos de endereço no formulário de Refugiado
    function limparCamposEndereco(formId) {
        $(`#${formId} input[name="logradouro"]`).val('');
        $(`#${formId} input[name="bairro"]`).val('');
        $(`#${formId} input[name="cidade"]`).val('');
        $(`#${formId} input[name="estado"]`).val(''); // Mesmo que invisível, é bom limpar
    }
    
    // Função de busca de CEP que será ativada ao tirar o foco do campo
    $('.cep-input').on('blur', function() {
        var $cepInput = $(this);
        var cep = $cepInput.val().replace(/\D/g, ''); 
        var formId = $cepInput.closest('form').attr('id'); // Pega o ID do formulário pai

        // Esta lógica de CEP só deve ser aplicada no formulário de Refugiado
        if (formId !== 'refugiado-form') {
            return;
        }

        if (cep.length != 8) {
            limparCamposEndereco(formId);
            return;
        }

        var url = 'https://viacep.com.br/ws/' + cep + '/json/';
        
        // Indicador de busca (opcional, mas bom para UX)
        $(`#${formId} input[name="logradouro"]`).val('Buscando...');
        
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                if (data.erro) {
                    alert("CEP não encontrado. Por favor, verifique.");
                    limparCamposEndereco(formId);
                } else {
                    // Preenche os campos do formulário Refugiado
                    $(`#${formId} input[name="logradouro"]`).val(data.logradouro);
                    $(`#${formId} input[name="bairro"]`).val(data.bairro);
                    $(`#${formId} input[name="cidade"]`).val(data.localidade);
                    $(`#${formId} input[name="estado"]`).val(data.uf);
                }
            },
            error: function() {
                alert("Erro ao buscar CEP. Tente novamente mais tarde.");
                limparCamposEndereco(formId);
            }
        });
    });

});