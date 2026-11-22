
/* =========================================
   H.H. INTER COLLEGE
   COMPLETE WEBSITE JAVASCRIPT
========================================= */

document.addEventListener("DOMContentLoaded", function () {


    /* =========================================
       1. MOBILE NAVIGATION
    ========================================= */

    const menuToggle = document.getElementById("menuToggle");
    const navLinks = document.getElementById("navLinks");

    if (menuToggle && navLinks) {

        menuToggle.addEventListener("click", function () {

            const isOpen = navLinks.classList.toggle("active");

            menuToggle.setAttribute(
                "aria-expanded",
                String(isOpen)
            );

        });

        // Close menu after clicking a navigation link

        navLinks.querySelectorAll("a").forEach(function (link) {

            link.addEventListener("click", function () {

                navLinks.classList.remove("active");

                menuToggle.setAttribute(
                    "aria-expanded",
                    "false"
                );

            });

        });

    }


    /* =========================================
       2. SUCCESS MESSAGE AUTO HIDE
    ========================================= */

    const successMessages = document.querySelectorAll(
        ".success-message"
    );

    successMessages.forEach(function (message) {

        setTimeout(function () {

            message.style.transition = "opacity 0.4s ease";
            message.style.opacity = "0";

            setTimeout(function () {
                message.remove();
            }, 450);

        }, 4000);

    });


/* =========================================
   3. COLLEGE GALLERY CAROUSEL
========================================= */

const memoryCarousel = document.getElementById(
    "memoryCarousel"
);

if (memoryCarousel) {

    const memorySlides = Array.from(
        memoryCarousel.querySelectorAll(".memory-slide")
    );

    const memoryDots = document.querySelector(
        ".memory-dots"
    );

    const memoryNext = memoryCarousel.querySelector(
        ".memory-next"
    );

    const memoryPrev = memoryCarousel.querySelector(
        ".memory-prev"
    );

    let memoryIndex = 0;

    let memoryAutoPlay = null;

    const totalMemorySlides = memorySlides.length;

    if (totalMemorySlides > 0) {

        // =====================================
        // CREATE GALLERY PAGINATION DOTS
        // =====================================

        if (memoryDots) {

            memoryDots.innerHTML = "";

            memorySlides.forEach(function (_, index) {

                const dot = document.createElement("button");

                dot.type = "button";

                dot.setAttribute(
                    "aria-label",
                    "Go to gallery image " + (index + 1)
                );

                if (index === 0) {
                    dot.classList.add("active");
                }

                dot.addEventListener("click", function () {

                    memoryIndex = index;

                    updateMemoryCarousel();

                    restartMemoryAutoPlay();

                });

                memoryDots.appendChild(dot);

            });

        }


        // =====================================
        // UPDATE GALLERY SLIDES
        // =====================================

        function updateMemoryCarousel() {

            memorySlides.forEach(function (slide) {

                slide.classList.remove(
                    "active",
                    "prev",
                    "next"
                );

            });

            const previousIndex =
                (memoryIndex - 1 + totalMemorySlides) %
                totalMemorySlides;

            const nextIndex =
                (memoryIndex + 1) % totalMemorySlides;


            // Active Center Slide

            memorySlides[memoryIndex].classList.add("active");


            // Previous Slide

            if (totalMemorySlides > 2) {

                memorySlides[previousIndex].classList.add(
                    "prev"
                );

            }


            // Next Slide

            if (totalMemorySlides > 1) {

                memorySlides[nextIndex].classList.add(
                    "next"
                );

            }


            // =====================================
            // UPDATE PAGINATION DOTS
            // =====================================

            if (memoryDots) {

                const dots = memoryDots.querySelectorAll(
                    "button"
                );

                dots.forEach(function (dot, index) {

                    dot.classList.toggle(
                        "active",
                        index === memoryIndex
                    );

                    dot.setAttribute(
                        "aria-current",
                        index === memoryIndex ? "true" : "false"
                    );

                });

            }

        }


        // =====================================
        // NEXT GALLERY IMAGE
        // =====================================

        function showNextMemory() {

            memoryIndex =
                (memoryIndex + 1) % totalMemorySlides;

            updateMemoryCarousel();

        }

        if (memoryNext) {

            memoryNext.addEventListener("click", function () {

                showNextMemory();

                restartMemoryAutoPlay();

            });

        }


        // =====================================
        // PREVIOUS GALLERY IMAGE
        // =====================================

        function showPreviousMemory() {

            memoryIndex =
                (memoryIndex - 1 + totalMemorySlides) %
                totalMemorySlides;

            updateMemoryCarousel();

        }

        if (memoryPrev) {

            memoryPrev.addEventListener("click", function () {

                showPreviousMemory();

                restartMemoryAutoPlay();

            });

        }


        // =====================================
        // GALLERY AUTO PLAY
        // =====================================

        function startMemoryAutoPlay() {

            stopMemoryAutoPlay();

            if (totalMemorySlides > 1) {

                memoryAutoPlay = setInterval(function () {

                    showNextMemory();

                }, 3500);

            }

        }


        // =====================================
        // STOP AUTO PLAY
        // =====================================

        function stopMemoryAutoPlay() {

            if (memoryAutoPlay) {

                clearInterval(memoryAutoPlay);

                memoryAutoPlay = null;

            }

        }


        // =====================================
        // RESTART AUTO PLAY
        // =====================================

        function restartMemoryAutoPlay() {

            startMemoryAutoPlay();

        }


        // =====================================
        // PAUSE ON MOUSE HOVER
        // =====================================

        memoryCarousel.addEventListener(
            "mouseenter",
            stopMemoryAutoPlay
        );


        // =====================================
        // RESUME ON MOUSE LEAVE
        // =====================================

        memoryCarousel.addEventListener(
            "mouseleave",
            startMemoryAutoPlay
        );


        // =====================================
        // PAUSE WHEN TAB IS HIDDEN
        // =====================================

        document.addEventListener("visibilitychange", function () {

            if (document.hidden) {

                stopMemoryAutoPlay();

            } else {

                startMemoryAutoPlay();

            }

        });


        // =====================================
        // INITIAL GALLERY SETUP
        // =====================================

        updateMemoryCarousel();

        startMemoryAutoPlay();

    }

}

/* =========================================
   END COLLEGE GALLERY CAROUSEL
========================================= */


    /* =========================================
       4. TEACHERS 3D COVERFLOW CAROUSEL
    ========================================= */

    const teachersCarousel = document.getElementById(
        "teachersCarousel"
    );

    if (teachersCarousel) {

        const teacherCards = Array.from(
            teachersCarousel.querySelectorAll(".carousel-card")
        );

        const teachersDots = document.getElementById(
            "teachersDots"
        );

        const teachersNext = teachersCarousel.querySelector(
            ".carousel-next"
        );

        const teachersPrev = teachersCarousel.querySelector(
            ".carousel-prev"
        );

        let teacherIndex = 0;

        let teacherAutoSlide = null;

        let isTeacherPaused = false;

        const totalTeachers = teacherCards.length;

        const reducedMotion = window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;


        if (totalTeachers > 0) {


            // Create Teacher Pagination Dots

            if (teachersDots) {

                teachersDots.innerHTML = "";

                teacherCards.forEach(function (_, index) {

                    const dot = document.createElement("button");

                    dot.type = "button";

                    dot.setAttribute(
                        "aria-label",
                        "Show teacher " + (index + 1)
                    );

                    dot.addEventListener("click", function () {

                        teacherIndex = index;

                        updateTeacherCarousel();

                        restartTeacherAutoplay();

                    });

                    teachersDots.appendChild(dot);

                });

            }


            // Update Teacher Carousel

            function updateTeacherCarousel() {

                teacherCards.forEach(function (card, index) {

                    card.classList.remove(
                        "is-center",
                        "is-left",
                        "is-right",
                        "is-hidden"
                    );

                    if (index === teacherIndex) {

                        card.classList.add("is-center");

                    }

                    else if (totalTeachers > 2) {

                        const previousIndex =
                            (teacherIndex - 1 + totalTeachers) %
                            totalTeachers;

                        const nextIndex =
                            (teacherIndex + 1) % totalTeachers;

                        if (index === previousIndex) {

                            card.classList.add("is-left");

                        }

                        else if (index === nextIndex) {

                            card.classList.add("is-right");

                        }

                        else {

                            card.classList.add("is-hidden");

                        }

                    }

                    else if (
                        totalTeachers === 2 &&
                        index === (teacherIndex + 1) % totalTeachers
                    ) {

                        card.classList.add("is-right");

                    }

                    else {

                        card.classList.add("is-hidden");

                    }

                });


                // Update Pagination Dots

                if (teachersDots) {

                    const dots = teachersDots.querySelectorAll(
                        "button"
                    );

                    dots.forEach(function (dot, index) {

                        const isActive = index === teacherIndex;

                        dot.classList.toggle(
                            "active",
                            isActive
                        );

                        dot.setAttribute(
                            "aria-current",
                            isActive ? "true" : "false"
                        );

                    });

                }

            }


            // Next Teacher

            function nextTeacher() {

                if (totalTeachers < 2) return;

                teacherIndex =
                    (teacherIndex + 1) % totalTeachers;

                updateTeacherCarousel();

            }


            // Previous Teacher

            function previousTeacher() {

                if (totalTeachers < 2) return;

                teacherIndex =
                    (teacherIndex - 1 + totalTeachers) %
                    totalTeachers;

                updateTeacherCarousel();

            }


            // Arrow Buttons

            if (teachersNext) {

                teachersNext.addEventListener("click", function () {

                    nextTeacher();

                    restartTeacherAutoplay();

                });

            }

            if (teachersPrev) {

                teachersPrev.addEventListener("click", function () {

                    previousTeacher();

                    restartTeacherAutoplay();

                });

            }


            // Clicking Side Cards

            teacherCards.forEach(function (card, index) {

                card.addEventListener("click", function (event) {

                    if (
                        event.target.closest(
                            "button, a, input"
                        )
                    ) {
                        return;
                    }

                    if (index !== teacherIndex) {

                        teacherIndex = index;

                        updateTeacherCarousel();

                        restartTeacherAutoplay();

                    }

                });

            });


            // Automatic Slide

            function startTeacherAutoplay() {

                stopTeacherAutoplay();

                if (totalTeachers < 2 || reducedMotion) {
                    return;
                }

                teacherAutoSlide = setInterval(function () {

                    if (
                        !isTeacherPaused &&
                        !document.hidden
                    ) {

                        nextTeacher();

                    }

                }, 4000);

            }


            // Stop Automatic Slide

            function stopTeacherAutoplay() {

                if (teacherAutoSlide !== null) {

                    clearInterval(teacherAutoSlide);

                    teacherAutoSlide = null;

                }

            }


            // Restart Automatic Slide

            function restartTeacherAutoplay() {

                startTeacherAutoplay();

            }


            // Pause on Mouse Hover

            teachersCarousel.addEventListener(
                "mouseenter",
                function () {

                    isTeacherPaused = true;

                }
            );

            teachersCarousel.addEventListener(
                "mouseleave",
                function () {

                    isTeacherPaused = false;

                }
            );


            // Pause While Keyboard-Focused

            teachersCarousel.addEventListener(
                "focusin",
                function () {

                    isTeacherPaused = true;

                }
            );

            teachersCarousel.addEventListener(
                "focusout",
                function () {

                    isTeacherPaused = false;

                }
            );


            // Initial Carousel Setup

            updateTeacherCarousel();

            startTeacherAutoplay();

        }

    }


    /* =========================================
       START: FACULTY CARD SCROLL REVEAL
    ========================================= */

    const teachersSection = document.getElementById("teachers");

    if (teachersSection) {

        const prefersReducedMotion = window.matchMedia &&
            window.matchMedia("(prefers-reduced-motion: reduce)").matches;

        if (prefersReducedMotion || !("IntersectionObserver" in window)) {

            teachersSection.classList.add("is-faculty-revealed");

        } else {

            teachersSection.classList.add("faculty-reveal-pending");

            const facultyRevealObserver = new IntersectionObserver(
                function (entries, observer) {

                    entries.forEach(function (entry) {

                        if (entry.isIntersecting) {

                            teachersSection.classList.add(
                                "is-faculty-revealed"
                            );
                            teachersSection.classList.remove(
                                "faculty-reveal-pending"
                            );
                            observer.unobserve(teachersSection);

                        }

                    });

                },
                {
                    threshold: 0.15,
                    rootMargin: "0px 0px -30px 0px"
                }
            );

            facultyRevealObserver.observe(teachersSection);

        }

    }

    /* END: FACULTY CARD SCROLL REVEAL */


    /* =========================================
       5. TEACHER DETAILS MODAL
    ========================================= */

    const teacherViewButtons = document.querySelectorAll(
        ".faculty-view-btn[data-modal]"
    );

    const teacherModals = document.querySelectorAll(
        ".faculty-modal"
    );

    let previousBodyOverflow = "";


    // Open Teacher Modal

    function openTeacherModal(modal) {

        if (!modal) return;

        closeAllTeacherModals();

        previousBodyOverflow = document.body.style.overflow;

        modal.classList.add("active");

        modal.setAttribute("aria-hidden", "false");

        document.body.style.overflow = "hidden";

    }


    // Close All Teacher Modals

    function closeAllTeacherModals() {

        teacherModals.forEach(function (modal) {

            modal.classList.remove("active");

            modal.setAttribute("aria-hidden", "true");

        });

        document.body.style.overflow = previousBodyOverflow;

    }


    // Open Modal Buttons

    teacherViewButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const modalId = button.getAttribute("data-modal");

            const modal = document.getElementById(modalId);

            openTeacherModal(modal);

        });

    });


    // Close Button and Outside Click

    teacherModals.forEach(function (modal) {

        const closeButton = modal.querySelector(
            ".faculty-modal-close"
        );

        if (closeButton) {

            closeButton.addEventListener("click", function () {

                closeAllTeacherModals();

            });

        }

        modal.addEventListener("click", function (event) {

            if (event.target === modal) {

                closeAllTeacherModals();

            }

        });

    });


    // Close Modal with Escape Key

    document.addEventListener("keydown", function (event) {

        if (event.key === "Escape") {

            closeAllTeacherModals();

        }

    });


    /* =========================================
       6. FOUR-SECTION PREMIUM SCROLL REVEALS
    ========================================= */

    const premiumRevealSelectors = [
        ".academics-section .academic-card",
        ".facilities-section .facility-card",
        ".announcement-section .announcement-card",
        ".contact-section .premium-reveal-panel"
    ];

    const premiumRevealElements = [];

    premiumRevealSelectors.forEach(function (selector) {

        document.querySelectorAll(selector).forEach(function (element) {

            if (!element.classList.contains("premium-reveal-card")) {
                element.classList.add("premium-reveal-panel");
            }

            premiumRevealElements.push(element);

        });

    });

    document.querySelectorAll(
        ".contact-section .contact-info-item"
    ).forEach(function (item) {

        item.classList.add("premium-reveal-item");
        premiumRevealElements.push(item);

    });

    // Assign a 100ms stagger within each relevant card grid or panel group.
    [
        ".academics-section .academic-card",
        ".facilities-section .facility-card",
        ".announcement-section .announcement-card"
    ].forEach(function (selector) {

        document.querySelectorAll(selector).forEach(function (element, index) {

            element.style.setProperty(
                "--reveal-delay",
                (index * 100) + "ms"
            );

        });

    });

    document.querySelectorAll(
        ".contact-section .contact-info-item"
    ).forEach(function (item, index) {

        item.style.setProperty(
            "--reveal-delay",
            (index * 100) + "ms"
        );

    });

    if ("IntersectionObserver" in window) {

        const premiumRevealObserver = new IntersectionObserver(
            function (entries, observer) {

                entries.forEach(function (entry) {

                    if (entry.isIntersecting) {

                        entry.target.classList.add(
                            "is-premium-visible"
                        );

                        observer.unobserve(entry.target);

                    }

                });

            },
            {
                threshold: 0.12,
                rootMargin: "0px 0px -35px 0px"
            }
        );

        premiumRevealElements.forEach(function (element) {

            premiumRevealObserver.observe(element);

        });

    } else {

        premiumRevealElements.forEach(function (element) {

            element.classList.add("is-premium-visible");

        });

    }


    /* =========================================
       7. WEBSITE JAVASCRIPT END
    ========================================= */

});
