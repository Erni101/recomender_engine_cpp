document.addEventListener('DOMContentLoaded', () => {
    const userIdInput = document.getElementById('userId');
    const getRecommendationsBtn = document.getElementById('getRecommendations');
    const loadingElement = document.getElementById('loading');
    const resultsElement = document.getElementById('results');
    const recommendationsList = document.getElementById('recommendationsList');
    const resultUserId = document.getElementById('resultUserId');
    const errorElement = document.getElementById('error');
    const errorMessage = document.getElementById('errorMessage');

    // Manejar clic en el botón de recomendaciones
    getRecommendationsBtn.addEventListener('click', fetchRecommendations);
    
    // También permitir presionar Enter en el input
    userIdInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            fetchRecommendations();
        }
    });

    async function fetchRecommendations() {
        const userId = userIdInput.value.trim();
        
        // Validación básica
        if (!userId) {
            showError('Por favor ingresa un ID de usuario');
            return;
        }

        // Mostrar loading y limpiar resultados anteriores
        loadingElement.classList.remove('hidden');
        resultsElement.classList.add('hidden');
        errorElement.classList.add('hidden');
        getRecommendationsBtn.disabled = true;

        try {
            const response = await fetch('/api/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_id: userId })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Error al obtener recomendaciones');
            }

            // Mostrar resultados
            displayResults(data);
        } catch (error) {
            showError(error.message || 'Ocurrió un error al procesar tu solicitud');
        } finally {
            loadingElement.classList.add('hidden');
            getRecommendationsBtn.disabled = false;
        }
    }

    function displayResults(data) {
        // Actualizar el ID de usuario mostrado
        resultUserId.textContent = data.user_id;
        
        // Limpiar lista de recomendaciones
        recommendationsList.innerHTML = '';
        
        // Agregar cada recomendación a la lista
        if (data.recommendations && data.recommendations.length > 0) {
            data.recommendations.forEach((rec, index) => {
                const item = document.createElement('div');
                item.className = 'recommendation-item fade-in';
                item.style.animationDelay = `${index * 0.1}s`;
                item.innerHTML = `
                    <div class="flex items-center">
                        <span class="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full mr-3">
                            ${index + 1}
                        </span>
                        <span>${rec}</span>
                    </div>
                `;
                recommendationsList.appendChild(item);
            });
        } else {
            recommendationsList.innerHTML = '<p class="text-gray-500">No se encontraron recomendaciones para este usuario.</p>';
        }
        
        // Mostrar la sección de resultados
        resultsElement.classList.remove('hidden');
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorElement.classList.remove('hidden');
        resultsElement.classList.add('hidden');
    }
});
