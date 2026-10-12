/**
 * New Balaji Packers and Movers - Frontend JavaScript
 * Includes:
 * 1. Interactive Shifting Price Calculator
 * 2. Live Review Star Rating Selector
 * 3. Booking form helpers & Web Share API
 */

document.addEventListener('DOMContentLoaded', function () {
    initPriceCalculator();
    initStarRatingSelector();
    initQuoteFormHelpers();
});

/* ==========================================================================
   FEATURE 1: INTERACTIVE PRICE CALCULATOR
   ========================================================================== */
function initPriceCalculator() {
    const calcForm = document.getElementById('priceCalculatorForm');
    if (!calcForm) return;

    const pickupSelect = document.getElementById('calc_pickup');
    const dropSelect = document.getElementById('calc_drop');
    const typeSelect = document.getElementById('calc_type');
    const packingSelect = document.getElementById('calc_packing');
    const floorSelect = document.getElementById('calc_floor');
    
    // Result display elements
    const priceDisplay = document.getElementById('calc_price_display');
    const freightDisplay = document.getElementById('calc_freight_display');
    const packingDisplay = document.getElementById('calc_packing_display');
    const laborDisplay = document.getElementById('calc_labor_display');
    const bookBtn = document.getElementById('calc_book_btn');

    // Base price configuration matrix (INR)
    const basePrices = {
        '1 BHK': { base: 3800, packing: 800, labor: 900 },
        '2 BHK': { base: 5800, packing: 1400, labor: 1400 },
        '3+ BHK': { base: 8900, packing: 2200, labor: 2000 },
        'Office': { base: 7500, packing: 1800, labor: 1800 },
        'Car Transport': { base: 4500, packing: 400, labor: 600 },
        'Single Item': { base: 1800, packing: 400, labor: 400 }
    };

    function calculatePrice() {
        const pickup = pickupSelect.value;
        const drop = dropSelect.value;
        const shiftType = typeSelect.value;
        const packingTier = packingSelect.value;
        const floorTier = floorSelect.value;

        const config = basePrices[shiftType] || basePrices['2 BHK'];

        // Determine route distance factor
        let distanceMultiplier = 1.0;
        const isSameCity = (pickup === drop);
        const isKeyHub = ['Vuyyuru', 'Vijayawada', 'Machilipatnam'].includes(pickup) && 
                         ['Vuyyuru', 'Vijayawada', 'Machilipatnam'].includes(drop);
        
        if (isSameCity) {
            distanceMultiplier = 0.85; // Local intra-city discount
        } else if (isKeyHub) {
            distanceMultiplier = 1.05; // Triangle route (Vuyyuru-Vijayawada-Machilipatnam)
        } else if (pickup.includes('Other') || drop.includes('Other') || 
                   pickup === 'Hyderabad' || drop === 'Hyderabad' || 
                   pickup === 'Visakhapatnam' || drop === 'Visakhapatnam') {
            distanceMultiplier = 2.4; // Intercity / Long-distance route
        } else {
            distanceMultiplier = 1.4; // Regional route
        }

        // Adjust based on packing tier
        let packingCost = config.packing;
        if (packingTier === 'premium') {
            packingCost += 1200; // 5-layer bubble wrap & stretch film
        }

        // Adjust based on floor / stairs labor
        let laborCost = config.labor;
        if (floorTier === 'stairs') {
            laborCost += 600; // Manual carry without lift
        }

        const freightCost = Math.round((config.base * distanceMultiplier) / 100) * 100;
        const subtotal = freightCost + packingCost + laborCost;

        const lowEst = Math.round((subtotal * 0.95) / 100) * 100;
        const highEst = Math.round((subtotal * 1.15) / 100) * 100;

        // Update UI
        if (priceDisplay) {
            priceDisplay.textContent = `₹${lowEst.toLocaleString('en-IN')} - ₹${highEst.toLocaleString('en-IN')}`;
        }
        if (freightDisplay) {
            freightDisplay.textContent = `₹${freightCost.toLocaleString('en-IN')}`;
        }
        if (packingDisplay) {
            packingDisplay.textContent = `₹${packingCost.toLocaleString('en-IN')}`;
        }
        if (laborDisplay) {
            laborDisplay.textContent = `₹${laborCost.toLocaleString('en-IN')}`;
        }

        // Update CTA link
        if (bookBtn) {
            const avgEstimate = Math.round((lowEst + highEst) / 2);
            bookBtn.href = `/quote/?pickup=${encodeURIComponent(pickup)}&drop=${encodeURIComponent(drop)}&item=${encodeURIComponent(shiftType)}&estimate=${avgEstimate}`;
        }
    }

    // Attach listeners to all inputs
    [pickupSelect, dropSelect, typeSelect, packingSelect, floorSelect].forEach(element => {
        if (element) {
            element.addEventListener('change', calculatePrice);
        }
    });

    // Run initial calculation
    calculatePrice();
}

/* ==========================================================================
   FEATURE 2: LIVE REVIEW STAR RATING SELECTOR
   ========================================================================= */
function initStarRatingSelector() {
    const starBox = document.getElementById('liveStarSelector');
    const ratingInput = document.getElementById('id_rating_input');
    const captionEl = document.getElementById('starRatingCaption');

    if (!starBox || !ratingInput) return;

    const stars = starBox.querySelectorAll('.star-icon');
    let currentRating = parseInt(ratingInput.value) || 5;

    const ratingDescriptions = {
        1: '★☆☆☆☆ (1/5) - Poor',
        2: '★★☆☆☆ (2/5) - Fair',
        3: '★★★☆☆ (3/5) - Good Service',
        4: '★★★★☆ (4/5) - Very Good & Prompt',
        5: '★★★★★ (5/5) - Excellent & Highly Recommended!'
    };

    function renderStars(ratingValue) {
        stars.forEach(star => {
            const val = parseInt(star.getAttribute('data-rating'));
            if (val <= ratingValue) {
                star.classList.remove('bi-star');
                star.classList.add('bi-star-fill', 'text-warning');
            } else {
                star.classList.remove('bi-star-fill', 'text-warning');
                star.classList.add('bi-star');
            }
        });
        if (captionEl) {
            captionEl.textContent = ratingDescriptions[ratingValue] || `${ratingValue} Stars`;
        }
    }

    // Initial display
    renderStars(currentRating);

    // Hover and Click handling
    stars.forEach(star => {
        star.addEventListener('mouseover', function () {
            const hoverVal = parseInt(this.getAttribute('data-rating'));
            renderStars(hoverVal);
        });

        star.addEventListener('mouseout', function () {
            renderStars(currentRating);
        });

        star.addEventListener('click', function () {
            currentRating = parseInt(this.getAttribute('data-rating'));
            ratingInput.value = currentRating;
            renderStars(currentRating);
            
            // Visual feedback bounce
            this.style.transform = 'scale(1.35)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 180);
        });
    });
}

/* ==========================================================================
   BOOKING FORM ITEM CHECKBOXES HELPER
   ========================================================================== */
function initQuoteFormHelpers() {
    const checkboxes = document.querySelectorAll('.item-checkbox-input');
    const hiddenItemsInput = document.getElementById('id_selected_items');

    if (checkboxes.length > 0 && hiddenItemsInput) {
        function syncItems() {
            const checkedValues = [];
            checkboxes.forEach(cb => {
                if (cb.checked) {
                    checkedValues.push(cb.value);
                }
            });
            hiddenItemsInput.value = checkedValues.join(', ');
        }

        checkboxes.forEach(cb => {
            cb.addEventListener('change', syncItems);
        });
        syncItems();
    }
}

/* ==========================================================================
   SHARE WEBSITE UTILITY
   ========================================================================== */
window.shareWebsite = function () {
    if (navigator.share) {
        navigator.share({
            title: 'New Balaji Packers and Movers',
            text: 'Safe Move ... Happy Home! Trusted Packers & Movers in Vuyyuru (Head Office), Vijayawada & Machilipatnam.',
            url: window.location.origin,
        }).catch(() => {});
    } else {
        navigator.clipboard.writeText(window.location.origin);
        alert('Website link copied to clipboard! Share it with friends and family.');
    }
};
