document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.querySelector("aside");
    if (!sidebar) return;

    // Create toggle button
    const toggleBtn = document.createElement("button");
    toggleBtn.innerHTML = "☰";
    toggleBtn.style.position = "fixed";
    toggleBtn.style.top = "15px";
    toggleBtn.style.left = "15px";
    toggleBtn.style.zIndex = "9999";
    toggleBtn.style.padding = "8px 12px";
    toggleBtn.style.background = "#111827";
    toggleBtn.style.color = "white";
    toggleBtn.style.border = "none";
    toggleBtn.style.borderRadius = "8px";
    toggleBtn.style.cursor = "pointer";

    document.body.appendChild(toggleBtn);

    // Restore saved state
    if (localStorage.getItem("sidebarCollapsed") === "true") {
        document.body.classList.add("sidebar-collapsed");
    }

    toggleBtn.addEventListener("click", function () {
        document.body.classList.toggle("sidebar-collapsed");

        localStorage.setItem(
            "sidebarCollapsed",
            document.body.classList.contains("sidebar-collapsed")
        );
    });
});