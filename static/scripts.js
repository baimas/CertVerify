let sortOrder = false;

function sortTable() {
    const table = document.querySelector("tbody");
    const rows = Array.from(table.querySelectorAll("tr"));
    sortOrder = !sortOrder;

    rows.sort((a, b) => {
        const aValue = parseInt(a.cells[3].innerText);
        const bValue = parseInt(b.cells[3].innerText);
        return sortOrder ? aValue - bValue : bValue - aValue;
    });

    rows.forEach(row => table.appendChild(row));
}
