/**
 * Feedback Dashboard - Frontend
 */

// Production: Update this URL after deploying backend to Render
const API_BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : 'https://YOUR_RENDER_APP_NAME.onrender.com';

// Submit review form handler
async function submitReview(event) {
    event.preventDefault();

    const form = document.getElementById('feedbackForm');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    const btnSpinner = document.getElementById('btnSpinner');
    const responseBox = document.getElementById('responseBox');

    const rating = parseInt(document.getElementById('rating').value);
    const review = document.getElementById('review').value.trim();

    if (!rating || rating < 1 || rating > 5) {
        showResponse('Please select a rating.', 'error');
        return;
    }

    if (!review) {
        showResponse('Please enter your review.', 'error');
        return;
    }

    if (review.length > 5000) {
        showResponse('Review is too long. Please keep it under 5000 characters.', 'error');
        return;
    }

    submitBtn.disabled = true;
    btnText.style.display = 'none';
    btnSpinner.style.display = 'inline-block';
    responseBox.classList.remove('visible', 'success', 'error');

    try {
        const response = await fetch(`${API_BASE_URL}/submit-review`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rating, review })
        });

        const data = await response.json();

        if (response.ok && data.status === 'success') {
            showResponse(data.ai_response, 'success');
            form.reset();
        } else {
            showResponse(data.detail || 'Failed to submit review. Please try again.', 'error');
        }
    } catch (error) {
        console.error('Submit error:', error);
        showResponse('Unable to connect to the server. Please check if the backend is running.', 'error');
    } finally {
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        btnSpinner.style.display = 'none';
    }
}

// Display response message
function showResponse(message, type) {
    const responseBox = document.getElementById('responseBox');
    const responseText = document.getElementById('responseText');

    responseText.textContent = message;
    responseBox.classList.remove('success', 'error');
    responseBox.classList.add('visible', type);
}

// Fetch reviews for admin dashboard
async function fetchReviews() {
    const refreshBtn = document.getElementById('refreshBtn');
    const refreshBtnText = document.getElementById('refreshBtnText');
    const refreshSpinner = document.getElementById('refreshSpinner');
    const reviewsBody = document.getElementById('reviewsBody');
    const reviewCount = document.getElementById('reviewCount');
    const emptyState = document.getElementById('emptyState');
    const tableContainer = document.querySelector('.table-container');

    if (refreshBtn) {
        refreshBtn.disabled = true;
        if (refreshBtnText) refreshBtnText.style.display = 'none';
        if (refreshSpinner) refreshSpinner.style.display = 'inline-block';
    }

    try {
        const response = await fetch(`${API_BASE_URL}/reviews`);

        if (!response.ok) throw new Error('Failed to fetch reviews');

        const reviews = await response.json();

        if (reviewCount) {
            reviewCount.textContent = `${reviews.length} review${reviews.length !== 1 ? 's' : ''} found`;
        }

        if (reviews.length === 0) {
            if (tableContainer) tableContainer.style.display = 'none';
            if (emptyState) emptyState.style.display = 'block';
            return;
        }

        if (tableContainer) tableContainer.style.display = 'block';
        if (emptyState) emptyState.style.display = 'none';

        if (reviewsBody) {
            reviewsBody.innerHTML = reviews.map(review => `
                <tr>
                    <td><span class="rating rating-${review.rating}">${review.rating}</span></td>
                    <td><div class="review-text truncated" title="${escapeHtml(review.review)}">${escapeHtml(review.review)}</div></td>
                    <td><div class="summary-text">${escapeHtml(review.ai_summary || 'Processing...')}</div></td>
                    <td><div class="action-text">${escapeHtml(review.recommended_action || 'Processing...')}</div></td>
                    <td><span class="timestamp">${formatDate(review.created_at)}</span></td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Fetch error:', error);
        if (reviewCount) {
            reviewCount.textContent = 'Error loading reviews. Is the backend running?';
        }
    } finally {
        if (refreshBtn) {
            refreshBtn.disabled = false;
            if (refreshBtnText) refreshBtnText.style.display = 'inline';
            if (refreshSpinner) refreshSpinner.style.display = 'none';
        }
    }
}

// Format date to readable string
function formatDate(isoString) {
    if (!isoString) return 'N/A';
    const date = new Date(isoString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize form handler
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('feedbackForm');
    if (form) {
        form.addEventListener('submit', submitReview);
    }
});
