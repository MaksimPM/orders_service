document.addEventListener("DOMContentLoaded", function () {
    let selectedOrderId = null;
    const modal = document.getElementById("status-modal");
    const statusSelect = document.getElementById("statusSelect");
    const saveButton = document.getElementById("saveStatus");
    const closeButton = document.getElementById("closeModal");

    document.querySelectorAll(".update-status").forEach(button => {
        button.addEventListener("click", function () {
            selectedOrderId = this.dataset.orderId;
            statusSelect.value = this.dataset.status;
            modal.style.display = "flex";
        });
    });

    closeButton.addEventListener("click", function () {
        modal.style.display = "none";
    });

    modal.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });

    saveButton.addEventListener("click", function (e) {
        e.preventDefault();
        fetch(`/update_status/${selectedOrderId}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
            },
            body: `status=${statusSelect.value}`
        }).then(response => {
            if (response.ok) {
                location.reload();
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    let selectedOrderId = null;
    const deleteModal = document.getElementById("delete-modal");
    const confirmDeleteButton = document.getElementById("confirmDelete");
    const cancelDeleteButton = document.getElementById("cancelDelete");

    document.querySelectorAll(".delete-order").forEach(button => {
        button.addEventListener("click", function () {
            selectedOrderId = this.dataset.orderId;
            deleteModal.style.display = "flex";
        });
    });

    confirmDeleteButton.addEventListener("click", function (e) {
        e.preventDefault();
        fetch(`/delete/${selectedOrderId}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
            }
        }).then(response => {
            if (response.ok) {
                location.reload();
            }
        });
    });

    cancelDeleteButton.addEventListener("click", function () {
        deleteModal.style.display = "none";
    });

    deleteModal.addEventListener("click", function (event) {
        if (event.target === deleteModal) {
            deleteModal.style.display = "none";
        }
    });
});

