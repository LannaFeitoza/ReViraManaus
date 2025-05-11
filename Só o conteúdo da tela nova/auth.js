function login(event) {
    event.preventDefault(); // Impede o envio do formulário para recarregar a página

    const email = document.getElementById('login-email').value;
    const senha = document.getElementById('login-password').value;

    const usuarios = JSON.parse(localStorage.getItem('usuarios')) || [];

    const usuario = usuarios.find(u => u.email === email && u.senha === senha);

    if (usuario) {
        localStorage.setItem('usuario', JSON.stringify(usuario));
        alert('Login realizado com sucesso!');
        window.location.href = 'tela_nova_minha_conta.html'; // Redireciona para a tela principal
    } else {
        alert('Credenciais incorretas. Tente novamente.');
    }
}
