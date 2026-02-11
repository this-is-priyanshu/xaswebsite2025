document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("expandedImg");
    const closeModal = document.querySelector(".close-modal");

    if (!modal || !modalImg) {
        console.error("Lightbox elements missing! Check your HTML IDs.");
        return;
    }

    const galleryImages = document.querySelectorAll(".gallery div img");

    galleryImages.forEach(img => {
        img.onclick = function() {
            modal.style.display = "flex";
            modalImg.src = this.src;
            document.body.style.overflow = "hidden"; 
        }
    });

    if (closeModal) {
        closeModal.onclick = function() {
            modal.style.display = "none";
            document.body.style.overflow = "auto";
        }
    }

    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
            document.body.style.overflow = "auto";
        }
    }
});