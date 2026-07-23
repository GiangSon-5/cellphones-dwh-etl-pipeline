/**
 * CellphoneS Analytics Engineering Presentation Dashboard
 * Main JavaScript Controller
 */

// Tab Switching Controller
function switchTab(tabId, btnElement) {
    // Hide all tab panels
    const panels = document.querySelectorAll('.tab-panel');
    panels.forEach(panel => panel.classList.remove('active'));

    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => btn.classList.remove('active'));

    // Activate target tab panel & button
    const targetPanel = document.getElementById(tabId);
    if (targetPanel) {
        targetPanel.classList.add('active');
    }
    if (btnElement) {
        btnElement.classList.add('active');
    }

    // Smooth scroll to top of content section
    window.scrollTo({ top: 360, behavior: 'smooth' });
}

// Accordion Toggle Controller
function toggleAccordion(headerElement) {
    const item = headerElement.parentElement;
    if (item) {
        item.classList.toggle('active');
    }
}

// Data Preview Toggle Controller
function toggleDataPreview() {
    const previewContainer = document.getElementById('sampleDataPreviewContainer');
    const toggleBtn = document.getElementById('togglePreviewBtn');
    if (previewContainer) {
        if (previewContainer.style.display === 'none') {
            previewContainer.style.display = 'block';
            if (toggleBtn) {
                toggleBtn.innerHTML = '<i class="fa-solid fa-eye-slash"></i> Ẩn Mẫu Xem Trước Dữ Liệu (5 Dòng)';
            }
        } else {
            previewContainer.style.display = 'none';
            if (toggleBtn) {
                toggleBtn.innerHTML = '<i class="fa-solid fa-eye"></i> Hiện Mẫu Xem Trước Dữ Liệu (5 Dòng)';
            }
        }
    }
}

// Initialize Interactive Animations on Load
document.addEventListener('DOMContentLoaded', () => {
    console.log('CellphoneS AE Presentation Dashboard Loaded Successfully.');
});
