/**
 * Astral Sport — Main JavaScript
 * Handles scroll animations and HTMX event listeners
 */

document.addEventListener('DOMContentLoaded', () => {
    // === Intersection Observer for Scroll Animations ===
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                entry.target.style.opacity = '1';

                // Apply staggered animations to children if they have delay classes
                const children = entry.target.querySelectorAll('[style*="animation-delay"]');
                children.forEach(child => {
                    child.style.opacity = '1';
                });

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all elements with animate-on-scroll class
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });

    // === HTMX Events ===
    document.body.addEventListener('htmx:afterSwap', (event) => {
        // Re-observe new elements that might have been added
        event.detail.target.querySelectorAll('.animate-on-scroll').forEach(el => {
            observer.observe(el);
        });
    });

    // === Chat Input — Auto-add user message bubble ===
    const chatForm = document.querySelector('[hx-post*="chat"]');
    if (chatForm) {
        chatForm.addEventListener('htmx:beforeRequest', (e) => {
            const input = chatForm.querySelector('input[name="message"]');
            const messagesDiv = document.getElementById('chat-messages');
            if (input && input.value.trim() && messagesDiv) {
                // Add user message bubble
                const userBubble = document.createElement('div');
                userBubble.className = 'flex gap-3 justify-end animate-slide-in-right';
                userBubble.innerHTML = `
                    <div class="bg-astral-black text-white rounded-2xl rounded-tr-sm px-4 py-3 max-w-[85%]">
                        <p class="text-sm leading-relaxed">${escapeHtml(input.value.trim())}</p>
                    </div>
                `;
                messagesDiv.appendChild(userBubble);

                // Add typing indicator
                const typingBubble = document.createElement('div');
                typingBubble.className = 'flex gap-3 animate-fade-in';
                typingBubble.id = 'typing-indicator';
                typingBubble.innerHTML = `
                    <div class="w-8 h-8 rounded-full bg-astral-black flex-shrink-0 flex items-center justify-center">
                        <span class="text-white text-xs font-bold">A</span>
                    </div>
                    <div class="bg-astral-gray-100 rounded-2xl rounded-tl-sm px-4 py-3">
                        <div class="flex gap-1.5">
                            <div class="w-2 h-2 bg-astral-gray-400 rounded-full animate-bounce" style="animation-delay: 0ms;"></div>
                            <div class="w-2 h-2 bg-astral-gray-400 rounded-full animate-bounce" style="animation-delay: 150ms;"></div>
                            <div class="w-2 h-2 bg-astral-gray-400 rounded-full animate-bounce" style="animation-delay: 300ms;"></div>
                        </div>
                    </div>
                `;
                messagesDiv.appendChild(typingBubble);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
        });

        chatForm.addEventListener('htmx:afterRequest', () => {
            // Remove typing indicator
            const typing = document.getElementById('typing-indicator');
            if (typing) typing.remove();

            const messagesDiv = document.getElementById('chat-messages');
            if (messagesDiv) {
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
        });
    }

    // === Navbar transparency handler (backup for Alpine) ===
    const navbar = document.querySelector('nav');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
});

/**
 * Escape HTML to prevent XSS in user message display
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
