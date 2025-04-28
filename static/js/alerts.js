function processFlashMessages(messages) {
    messages.forEach(function([category, message]) {
      if (category === 'success') {
        Swal.fire({
          icon: 'success',
          title: 'Sucesso!',
          text: message,
          confirmButtonColor: '#3085d6'
        });
      } else if (category === 'error') {
        Swal.fire({
          icon: 'error',
          title: 'Erro!',
          text: message,
          confirmButtonColor: '#d33'
        });
      }
    });
  }
  
  function confirmarExclusao(nome) {
    Swal.fire({
      title: 'Tem certeza?',
      text: `Tem certeza que deseja excluir ${nome}?`,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'OK',
      cancelButtonText: 'Cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        window.location.href = `/excluir/${nome}`;
      }
    });
  }
  