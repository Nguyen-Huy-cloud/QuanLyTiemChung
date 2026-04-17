document.addEventListener('DOMContentLoaded', function() {
    // Tìm ô nhập ngày tiêm và ô phản ứng trong form
    const injectionDateInput = document.querySelector('input[type="date"]');
    const reactionTextarea = document.querySelector('textarea[name="reaction"]');

    if (injectionDateInput) {
        injectionDateInput.addEventListener('change', function() {
            const selectedDate = new Date(this.value);
            if (!isNaN(selectedDate)) {
                // Giả sử khoảng cách giữa 2 mũi tiêm là 28 ngày (4 tuần)
                selectedDate.setDate(selectedDate.getDate() + 28);
                
                const day = String(selectedDate.getDate()).padStart(2, '0');
                const month = String(selectedDate.getMonth() + 1).padStart(2, '0');
                const year = selectedDate.getFullYear();
                
                // Gợi ý ngày tiêm nhắc lại vào ô phản ứng hoặc thông báo cho người dùng
                const suggestMsg = `Gợi ý: Mũi tiếp theo vào ngày ${day}/${month}/${year}`;
                if (reactionTextarea) {
                    reactionTextarea.placeholder = suggestMsg;
                    console.log(suggestMsg);
                }
            }
        });
    }
});