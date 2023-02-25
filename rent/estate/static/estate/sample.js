const openModalButtons = document.querySelectorAll('[data-popup-target]')
const closeModalButtons = document.querySelectorAll('[data-close-link]')
const overlay = document.getElementById('overlay-filter')


openModalButtons.forEach(button => {
    button.addEventListener('click', () => {
        const popup = document.querySelector(button.dataset.modalTarget)
        openModal(popup)
    })
})

overlay_filter.addEventListener('click', () => {
    const modals = document.querySelectorAll('.popup.active')
    modals.forEach(popup => {
        closeModal(popup)
    })
})

closeModalButtons.forEach(button => {
    button.addEventListener('click', () => {
        const popup = button.closest('.popup')
        closeModal(popup)
    })
})

function openModal(popup) {
    if (popup == null) return
    popup.classList.add('active')
    overlay.classList.add('active')
}

function closeModal(popup) {
    if (popup == null) return
    popup.classList.remove('active')
    overlay.classList.remove('active')
}