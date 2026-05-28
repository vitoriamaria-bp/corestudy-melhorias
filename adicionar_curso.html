document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-search-input]").forEach((input) => {
        const targetId = input.dataset.searchInput;
        const target = document.querySelector(`[data-search-target="${targetId}"]`);

        if (!target) {
            return;
        }

        const items = Array.from(target.querySelectorAll("[data-search-item]"));

        input.addEventListener("input", () => {
            const term = input.value.trim().toLowerCase();

            items.forEach((item) => {
                const content = item.textContent.toLowerCase();
                item.hidden = term !== "" && !content.includes(term);
            });
        });
    });

    document.querySelectorAll("[data-sort-option]").forEach((button) => {
        button.addEventListener("click", () => {
            const targetId = button.dataset.sortTarget;
            const mode = button.dataset.sortOption;
            const target = document.querySelector(`[data-search-target="${targetId}"]`);

            if (!target) {
                return;
            }

            const items = Array.from(target.querySelectorAll("[data-search-item]"));

            items.sort((a, b) => {
                const idA = Number(a.dataset.sortId || 0);
                const idB = Number(b.dataset.sortId || 0);
                const nameA = (a.dataset.sortName || a.textContent).trim().toLowerCase();
                const nameB = (b.dataset.sortName || b.textContent).trim().toLowerCase();

                if (mode === "latest") {
                    return idB - idA;
                }

                if (mode === "oldest") {
                    return idA - idB;
                }

                return nameA.localeCompare(nameB);
            });

            items.forEach((item) => target.appendChild(item));

            const menu = button.closest("details");
            if (menu) {
                menu.removeAttribute("open");
            }
        });
    });
});
