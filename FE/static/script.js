document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('testCaseForm');
    const submitBtn = document.getElementById('submitBtn');
    const clearBtn = document.getElementById('clearBtn');
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const promptInput = document.getElementById('prompt');
    const userStoryInput = document.getElementById('user_story');

    // Tab switching
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            if (btn.dataset.tab === 'default') {
                promptInput.value = getDefaultPrompt();
                promptInput.disabled = true;
            } else {
                promptInput.value = '';
                promptInput.disabled = false;
            }
        });
    });

    // Clear button
    clearBtn.addEventListener('click', () => {
        promptInput.value = '';
        userStoryInput.value = '';
        error.classList.add('hidden');
    });

    // Form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        
        try {
            loading.classList.remove('hidden');
            error.classList.add('hidden');
            submitBtn.disabled = true;
            clearBtn.disabled = true;
            
            const response = await fetch('/generate', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.error || 'Failed to generate test cases');
            }
            
            const blob = await response.blob();
            
            // Download file
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'test_cases.xlsx';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();
            
        } catch (err) {
            error.textContent = err.message;
            error.classList.remove('hidden');
        } finally {
            loading.classList.add('hidden');
            submitBtn.disabled = false;
            clearBtn.disabled = false;
        }
    });

    function getDefaultPrompt() {
        return `Generate test cases for the following user story:

Instructions:
1. Each test case should be on a new line
2. Start each test case with a number
3. Be specific and detailed
4. Include positive and negative scenarios
5. Consider edge cases and validations
6. For tables, include data validation cases

{user_story}`;
    }
}); 