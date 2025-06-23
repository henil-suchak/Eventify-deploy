let scanner;

function openScanner() {
    document.getElementById("qrScannerModal").classList.remove("hidden");
    startQRScanner();
}

function closeScanner() {
    document.getElementById("qrScannerModal").classList.add("hidden");
    if (scanner) {
        scanner.stop().catch(err => console.error("Error stopping scanner:", err));
    }
}

function startQRScanner() {
    scanner = new Html5QrcodeScanner("qr-video", { fps: 10, qrbox: 250 });

    scanner.render((decodedText) => {
        fetch("/event/scan_attendee/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ qr_code: decodedText })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Server response not OK");
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            closeScanner();
            location.reload();
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Failed to scan QR code. Please try again.");
        });
    }, (errorMessage) => {
        console.error("QR Scanner Error:", errorMessage);
        alert("Scanning error: " + errorMessage);
    });
}