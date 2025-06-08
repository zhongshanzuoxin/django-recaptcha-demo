document.addEventListener('DOMContentLoaded', function() {
    initGuideSwiper();
    initVideoModals();
    initSpecNavigation();
    initFixedMessages();
    initFeatureAnimations();
    initCaseStudyCarousel();
    initSmoothAnimations();
    initRevenueFlowAnimations();
    initRevenueCardAnimations();
    initSetupFlowAlternate();
    initHeroAnimation();
    initFanMonetizationAnimations();
    initAfterLaunchAnimations();
    initRevenueCTAAnimation();
    initUnifiedCTAAnimation();
});

// Topガイドスライダー
function initGuideSwiper() {
  const swiperElement = document.querySelector('.guide-swiper');
  if (!swiperElement) return;

  return new Swiper('.guide-swiper', {
      slidesPerView: 'auto',
      spaceBetween: 20,
      loop: true,
      autoplay: {
          delay: 0,
          disableOnInteraction: false,
      },
      speed: 5000,
      allowTouchMove: true,
      pauseOnMouseEnter: true
  });
}


// 機能紹介ページに載せるアコーディオン
$(document).ready(function() {
    var speed = 300;
    
    $('.js-details-summary').on("click", function(event) {
      event.preventDefault();
      var $header = $(this);
      var $content = $header.next('.js-details-content');

      $header.toggleClass("is-active");

      if ($content.is(":visible")) {
        $content.slideUp(speed);
      } else {
        $content.hide().slideDown(speed);
      }
    });
});


// ビデオモーダル関数
function initVideoModals() {
  // 各モーダルの設定を配列で定義
  const modalConfigs = [
    {
      modalId: 'videoModal',
      videoId: 'modalVideo',
      openFuncName: 'openVideoModal',
      closeFuncName: 'closeVideoModal'
    },
    {
      modalId: 'afterLaunchVideoModal',
      videoId: 'afterLaunchModalVideo',
      openFuncName: 'openAfterLaunchVideoModal',
      closeFuncName: 'closeAfterLaunchVideoModal'
    }
    // 必要に応じて他のモーダル設定を追加
  ];
  
  // 各モーダルを初期化
  modalConfigs.forEach(config => {
    const modal = document.getElementById(config.modalId);
    const video = document.getElementById(config.videoId);
    
    if (!modal || !video) return;
    
    // 開く関数
    window[config.openFuncName] = function() {
      if (config.modalId === 'afterLaunchVideoModal') {
        modal.style.display = 'flex';
      } else {
        modal.style.display = 'block';
      }
      video.play();
      document.body.style.overflow = 'hidden';
    };
    
    // 閉じる関数
    window[config.closeFuncName] = function() {
      modal.style.display = 'none';
      video.pause();
      video.currentTime = 0;
      document.body.style.overflow = '';
    };
    
    // モーダル外クリックで閉じる
    modal.addEventListener('click', function(e) {
      if (e.target === modal) {
        window[config.closeFuncName]();
      }
    });
  });
}


// 機能説明ページの順序
const SPEC_PAGES = [
  { path: 'room', title: 'ルーム機能' },
  { path: 'live', title: 'ライブ機能' },
  { path: 'goods_shop', title: 'ショップ機能（グッズ）' },
  { path: 'digital_goods_shop', title: 'ショップ機能（デジタル）' },
  { path: '2shot_shop', title: 'ショップ機能（2shot）' },
  { path: 'dm', title: 'DM機能' },
  { path: '2shot', title: '2shot機能' },
  { path: 'moderation', title: 'ミュート・ユーザー制限機能' },
  { path: 'delivery_management', title: '配送管理機能' },
  { path: 'permission_management', title: '権限管理機能' },
  { path: 'account_management', title: 'アカウント管理機能' },
  { path: 'permissions_overview', title: '権限について' },
  { path: 'timeline', title: 'タイムライン機能' },
  { path: 'collection', title: 'コレクション機能' }
];



// 機能説明ナビゲーション
function initSpecNavigation() {
  const currentPath = window.location.pathname.split('/').filter(Boolean).pop();
  const currentIndex = SPEC_PAGES.findIndex(page => page.path === currentPath);
  
  if (currentIndex === -1) return;

  // インデックスの計算
  const prevIndex = currentIndex === 0 ? SPEC_PAGES.length - 1 : currentIndex - 1;
  const nextIndex = currentIndex === SPEC_PAGES.length - 1 ? 0 : currentIndex + 1;

  const prevPage = SPEC_PAGES[prevIndex];
  const nextPage = SPEC_PAGES[nextIndex];

  const navLinks = document.querySelector('.spec-nav-links');
  if (!navLinks) return;

  navLinks.innerHTML = `
      <a href="/functional_specs/${prevPage.path}" class="spec-nav-link prev">
          <span class="nav-label">前の記事</span>
          <span class="nav-title">${prevPage.title}</span>
      </a>
      <a href="/functional_specs/${nextPage.path}" class="spec-nav-link next">
          <span class="nav-label">次の記事</span>
          <span class="nav-title">${nextPage.title}</span>
      </a>
  `;
}


// 固定のメッセージ
function initFixedMessages() {
    const messages = document.querySelectorAll('.fixed-message-container .message');
    messages.forEach(function(message) {
        setTimeout(function() {
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000); // 5秒後にメッセージを消す
    });
}



// Topの機能紹介ナビゲーションの動き
function initFeatureAnimations() {
  const featureBlocks = document.querySelectorAll('.feature-block');

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const target = entry.target;
          target.style.opacity = '1';
          target.style.transform = 'translateX(0)';
        }
      });
    },
    { threshold: 0.1 }
  );

  featureBlocks.forEach((block, index) => {
    const featureContent = block.querySelector('.feature-content');
    
    if (featureContent) {
      // 各コンテンツ内の要素配置を確認
      const imageElement = featureContent.querySelector('.feature-image');
      const textElement = featureContent.querySelector('.text-content');
      
      if (imageElement && textElement) {
        const imageIndex = Array.from(featureContent.children).indexOf(imageElement);
        const textIndex = Array.from(featureContent.children).indexOf(textElement);
        const isImageLeft = imageIndex < textIndex;
        
        // 画像が左側にある場合は右から、テキストが左側にある場合は左からアニメーション
        featureContent.style.opacity = '0';
        featureContent.style.transform = isImageLeft ? 'translateX(-50px)' : 'translateX(50px)';
        featureContent.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        featureContent.style.transitionDelay = '250ms';
      }
      
      observer.observe(featureContent);
    }
  });
  
  // タイトルのアニメーション
  const featuresTitle = document.querySelector('.features-detail-title');
  if (featuresTitle) {
    featuresTitle.style.opacity = '0';
    featuresTitle.style.transform = 'translateY(20px)';
    featuresTitle.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    
    observer.observe(featuresTitle);
  }
}



// 事例のカルーセル
function initCaseStudyCarousel() {
  const carousel = document.querySelector('.case-study-carousel');
  if (!carousel) return;
  
  const slides = document.querySelectorAll('.case-study-slide');
  const prevButton = document.querySelector('.case-study-nav-button.prev');
  const nextButton = document.querySelector('.case-study-nav-button.next');
  let currentIndex = 0;
  const slideCount = slides.length;
  
  // スライドを更新する関数
  function updateCarousel() {

      const slideWidth = document.querySelector('.case-study-slide').offsetWidth;

      const computedStyle = window.getComputedStyle(carousel);
      const gapPx = parseInt(computedStyle.gap);
      
      // 画面幅に応じて最大インデックスを設定
      let maxVisibleIndex;
      if (window.innerWidth <= 768) {
          maxVisibleIndex = slideCount - 1;
      } else {
          maxVisibleIndex = slideCount - 2;
      }

      if (currentIndex > maxVisibleIndex) {
          currentIndex = 0;
      } else if (currentIndex < 0) {
          currentIndex = maxVisibleIndex;
      }

      const offset = currentIndex * (slideWidth + gapPx);
      carousel.style.transform = `translateX(-${offset}px)`;
  }
  
  prevButton.addEventListener('click', function() {
      currentIndex--;
      updateCarousel();
  });
  
  nextButton.addEventListener('click', function() {
      currentIndex++;
      updateCarousel();
  });
  
  // スワイプ対応（タッチデバイス用）
  let startX, moveX;
  const threshold = 100;
  
  carousel.addEventListener('touchstart', function(e) {
      startX = e.touches[0].clientX;
  });
  
  carousel.addEventListener('touchmove', function(e) {
      moveX = e.touches[0].clientX;
  });
  
  carousel.addEventListener('touchend', function(e) {
      if (!startX || !moveX) return;
      
      const diff = startX - moveX;
      
      if (Math.abs(diff) > threshold) {
          if (diff > 0) {
              currentIndex++;
          } else {
              currentIndex--;
          }
          updateCarousel();
      }
      
      startX = null;
      moveX = null;
  });
  
  // 自動スライド設定
  let autoSlide = setInterval(function() {
      currentIndex++;
      updateCarousel();
  }, 5000);
  
  // ユーザーがナビゲーションボタンをクリックしたら自動スライドを一時停止
  const carouselContainer = document.querySelector('.case-study-carousel-container');
  if (carouselContainer) {
    carouselContainer.addEventListener('mouseenter', function() {
        clearInterval(autoSlide);
    });
    
    // マウスが離れたら自動スライドを再開
    carouselContainer.addEventListener('mouseleave', function() {
        autoSlide = setInterval(function() {
            currentIndex++;
            updateCarousel();
        }, 5000);
    });
  }
  
  updateCarousel();
  
  window.addEventListener('resize', function() {
      updateCarousel();
  });
}





// サービスの特徴セクションのアニメーション
function initSmoothAnimations() {
  const animatedElements = new WeakSet();
  const observerOptions = {
      threshold: 0.15,
      rootMargin: '-50px 0px -50px 0px'
  };
  let observer;

  init();

  function init() {
      observer = new IntersectionObserver(
          handleIntersection, 
          observerOptions
      );

      if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', () => startObserving());
      } else {
          startObserving();
      }
  }

  function startObserving() {
      // タイトルの監視
      const title = document.querySelector('.service-features-title');
      if (title) observer.observe(title);

      // セクションの監視
      const sections = document.querySelectorAll('.service-feature-section');
      sections.forEach(section => observer.observe(section));
  }

  function handleIntersection(entries) {
      entries.forEach(entry => {
          if (entry.isIntersecting && !animatedElements.has(entry.target)) {
              animatedElements.add(entry.target);
              
              if (entry.target.classList.contains('service-features-title')) {
                  animateTitle(entry.target);
              } else if (entry.target.classList.contains('service-feature-section')) {
                  animateSection(entry.target);
              }
              
              // 一度アニメーションした要素は監視を停止
              observer.unobserve(entry.target);
          }
      });
  }

  function animateTitle(element) {
      animateElement(element, {
          opacity: [0, 1],
          transform: ['translateY(30px)', 'translateY(0px)']
      }, {
          duration: 800,
          easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
      });
  }

  function animateSection(section) {
      // セクション全体のアニメーション
      animateElement(section, {
          opacity: [0, 1],
          transform: ['translateY(40px) scale(0.95)', 'translateY(0px) scale(1)']
      }, {
          duration: 800,
          easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
      });

      // 背景のアニメーション
      const beforeElement = section;
      setTimeout(() => {
          beforeElement.style.setProperty('--before-opacity', '1');
          const before = window.getComputedStyle(beforeElement, '::before');
          animateElement(beforeElement, {
              '--before-opacity': [0, 1]
          }, { duration: 600 });
      }, 100);

      // 個別要素のアニメーション
      animateSectionElements(section);
  }

  function animateSectionElements(section) {
      const animations = [
          { selector: '.feature-number', delay: 200, animation: animateNumber },
          { selector: '.feature-label', delay: 300, animation: animateLabel },
          { selector: '.feature-title', delay: 400, animation: animateTitle },
          { selector: '.feature-visual', delay: 500, animation: animateVisual },
          { selector: '.feature-description', delay: 600, animation: animateDescription }
      ];

      animations.forEach(({ selector, delay, animation }) => {
          const element = section.querySelector(selector);
          if (element) {
              setTimeout(() => animation(element), delay);
          }
      });

      // リストアイテムのアニメーション
      setTimeout(() => animateListItems(section), 700);
  }

  function animateNumber(element) {
      animateElement(element, {
          opacity: [0.6, 1],
          transform: ['scale(0.8)', 'scale(1)']
      }, {
          duration: 800,
          easing: 'cubic-bezier(0.34, 1.56, 0.64, 1)'
      });
  }

  function animateLabel(element) {
      animateElement(element, {
          opacity: [0, 1],
          transform: ['translateX(-20px)', 'translateX(0px)']
      }, { duration: 600 });
  }

  function animateVisual(element) {
      animateElement(element, {
          opacity: [0, 1],
          transform: ['scale(0.8)', 'scale(1)']
      }, {
          duration: 800,
          easing: 'cubic-bezier(0.34, 1.56, 0.64, 1)'
      });

      // アイコン内部の要素
      const icon = element.querySelector('.feature-icon');
      if (icon) {
          setTimeout(() => animateIconElements(icon), 200);
      }
  }

  function animateIconElements(icon) {
      // 画像をアニメーション
      const img = icon.querySelector('img');
      if (img) {
          setTimeout(() => {
              animateElement(img, {
                  opacity: [0, 1],
                  transform: ['scale(0.7)', 'scale(1)']
              }, {
                  duration: 800,
                  easing: 'cubic-bezier(0.34, 1.56, 0.64, 1)'
              });
          }, 200);
      }

      // アイコンのアニメーション
      const caption = icon.parentElement.querySelector('.icon-caption');
      if (caption) {
          setTimeout(() => {
              animateElement(caption, {
                  opacity: [0, 1],
                  transform: ['translateY(10px)', 'translateY(0px)']
              }, { duration: 600 });
          }, 300);
      }
  }

  function animateDescription(element) {
      animateElement(element, {
          opacity: [0, 1],
          transform: ['translateX(30px)', 'translateX(0px)']
      }, {
          duration: 800,
          easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
      });
  }

  function animateListItems(section) {
      const listItems = section.querySelectorAll('.feature-list-items li');
      listItems.forEach((item, index) => {
          setTimeout(() => {
              animateElement(item, {
                  opacity: [0, 1],
                  transform: ['translateX(20px)', 'translateX(0px)']
              }, { duration: 500 });

              // ドットのアニメーション
              setTimeout(() => {
                  item.classList.add('animated');
              }, 200);
          }, index * 100);
      });
  }

  function animateElement(element, keyframes, options = {}) {
      if (!element || !element.animate) return;

      const defaultOptions = {
          duration: 600,
          easing: 'ease-out',
          fill: 'forwards'
      };

      const animationOptions = { ...defaultOptions, ...options };

      try {
          const animation = element.animate(keyframes, animationOptions);
          
          // アニメーション完了後にスタイルを適用
          animation.addEventListener('finish', () => {
              Object.keys(keyframes).forEach(property => {
                  const values = keyframes[property];
                  const finalValue = values[values.length - 1];
                  
                  if (property.startsWith('--')) {
                      element.style.setProperty(property, finalValue);
                  } else {
                      element.style[property] = finalValue;
                  }
              });
          });

          return animation;
      } catch (error) {
          fallbackAnimation(element, keyframes);
      }
  }

  function fallbackAnimation(element, keyframes) {
      Object.keys(keyframes).forEach(property => {
          const values = keyframes[property];
          const finalValue = values[values.length - 1];
          
          if (property.startsWith('--')) {
              element.style.setProperty(property, finalValue);
          } else {
              element.style[property] = finalValue;
          }
      });
  }
}







// 収益フローのアニメーション
function initRevenueFlowAnimations() {
    let isAnimating = false;
    
    let hasExecutedOnce = false;
    let hasTextAnimationsExecuted = false;
    
    const observerOptions = {
        threshold: 0.15,
        rootMargin: '-50px 0px -50px 0px'
    };

    // ページロード時の初期化を確実に行う
    function ensureInitialState() {
        const title = document.querySelector('.revenue-title');
        const description = document.querySelector('.revenue-description');
        const subDescription = document.querySelector('.revenue-sub-description');
        
        if (title && !title.style.opacity) {
            title.style.opacity = '0';
            title.style.transform = 'translateY(30px)';
        }
        
        if (description && !description.style.opacity) {
            description.style.opacity = '0';
            description.style.transform = 'translateY(30px)';
        }
        
        if (subDescription && !subDescription.style.opacity) {
            subDescription.style.opacity = '0';
            subDescription.style.transform = 'translateY(30px)';
        }
    }

    // 要素が既に表示領域にある場合の処理
    function checkElementsInView() {
        const title = document.querySelector('.revenue-title');
        const description = document.querySelector('.revenue-description');
        const subDescription = document.querySelector('.revenue-sub-description');
        
        const elements = [
            { element: title, delay: 0 },
            { element: description, delay: 200 },
            { element: subDescription, delay: 400 }
        ];
        
        elements.forEach(({ element, delay }) => {
            if (element) {
                const rect = element.getBoundingClientRect();
                const isInView = rect.top < window.innerHeight && rect.bottom > 0;
                
                if (isInView && element.style.opacity === '0') {
                    // 要素が見えているのに非表示の場合は、すぐにアニメーションを実行
                    setTimeout(() => {
                        animateTextElement(element, 0);
                    }, delay);
                }
            }
        });
    }

    function resetAnimation() {
        const steps = document.querySelectorAll('.revenue-step-simple');
        const connectors = document.querySelectorAll('.step-connector');
        
        steps.forEach(step => {
            step.style.opacity = '0';
        });
        
        connectors.forEach(connector => {
            const line = connector.querySelector('.step-connector-line');
            const arrow = connector.querySelector('.step-connector-arrow');
            
            if (line) {
                line.style.width = '';
                line.style.height = '';
                if (window.innerWidth <= 768) {
                    line.style.height = '0';
                } else {
                    line.style.width = '0';
                }
            }
            
            if (arrow) {
                arrow.style.opacity = '0';
                arrow.style.transform = 'scale(0)';
            }
        });

        const mobileItems = document.querySelectorAll('.mobile-revenue-item');
        const mobileArrows = document.querySelectorAll('.mobile-arrow');
        
        mobileItems.forEach(item => {
            item.style.opacity = '0';
        });
        
        mobileArrows.forEach(arrow => {
            arrow.style.opacity = '0';
            arrow.classList.remove('show');
        });
    }

    function showStep(stepIndex, delay = 0) {
        setTimeout(() => {
            const step = document.querySelector(`[data-step="${stepIndex}"]`);
            if (step) {
                step.style.opacity = '1';
            }
        }, delay);
    }

    function showConnector(connectorIndex, delay = 0) {
        setTimeout(() => {
            const connector = document.querySelector(`[data-connector="${connectorIndex}"]`);
            if (connector) {
                const line = connector.querySelector('.step-connector-line');
                const arrow = connector.querySelector('.step-connector-arrow');
                
                if (line) {
                    line.offsetHeight;
                    
                    if (window.innerWidth <= 768) {
                        line.style.height = '100%';
                    } else {
                        line.style.width = '100%';
                    }
                }
                
                if (arrow) {
                    setTimeout(() => {
                        arrow.style.opacity = '1';
                        arrow.style.transform = 'scale(1)';
                    }, 300);
                }
            }
        }, delay);
    }

    function showMobileStep(stepIndex, delay = 0) {
        setTimeout(() => {
            const step = document.querySelector(`[data-mobile-step="${stepIndex}"]`);
            if (step) {
                step.style.opacity = '1';
            }
        }, delay);
    }

    function showMobileArrow(arrowIndex, delay = 0) {
        setTimeout(() => {
            const arrow = document.querySelector(`[data-mobile-arrow="${arrowIndex}"]`);
            if (arrow) {
                arrow.style.opacity = '1';
                setTimeout(() => {
                    arrow.classList.add('show');
                }, 100);
            }
        }, delay);
    }

    function startAnimation() {
        if (hasExecutedOnce || isAnimating) {
            return;
        }
        
        hasExecutedOnce = true;
        isAnimating = true;
        resetAnimation();
        
        if (window.innerWidth <= 768) {
            // モバイル用アニメーション
            const mobileSequence = [
                { type: 'mobile-step', index: 0, delay: 100 },
                { type: 'mobile-arrow', index: 0, delay: 400 },
                { type: 'mobile-step', index: 1, delay: 700 },
                { type: 'mobile-arrow', index: 1, delay: 1000 },
                { type: 'mobile-step', index: 2, delay: 1300 },
                { type: 'mobile-arrow', index: 2, delay: 1600 },
                { type: 'mobile-step', index: 3, delay: 1900 }
            ];
            
            mobileSequence.forEach(item => {
                if (item.type === 'mobile-step') {
                    showMobileStep(item.index, item.delay);
                } else if (item.type === 'mobile-arrow') {
                    showMobileArrow(item.index, item.delay);
                }
            });
            
            setTimeout(() => {
                const finalStep = document.querySelector('[data-mobile-step="3"] .mobile-step-icon');
                if (finalStep) {
                    finalStep.style.animation = 'softPulse 2s ease-in-out infinite';
                }
                isAnimating = false;
            }, 2500);
        } else {
            // デスクトップ用アニメーション
            const sequence = [
                { type: 'step', index: 0, delay: 100 },
                { type: 'connector', index: 0, delay: 500 },
                { type: 'step', index: 1, delay: 900 },
                { type: 'connector', index: 1, delay: 1400 },
                { type: 'step', index: 2, delay: 1800 },
                { type: 'connector', index: 2, delay: 2300 },
                { type: 'step', index: 3, delay: 2700 }
            ];
            
            sequence.forEach(item => {
                if (item.type === 'step') {
                    showStep(item.index, item.delay);
                } else {
                    showConnector(item.index, item.delay);
                }
            });
            
            setTimeout(() => {
                const finalStep = document.querySelector('[data-step="3"] .step-icon-container');
                if (finalStep) {
                    finalStep.style.animation = 'softPulse 2s ease-in-out infinite';
                }
                isAnimating = false;
            }, 3200);
        }
    }

    function initializeRevenueFlow() {
        resetAnimation();
    }

    function animateElement(element, keyframes, options = {}) {
        if (!element || !element.animate) return;

        const defaultOptions = {
            duration: 600,
            easing: 'ease-out',
            fill: 'forwards'
        };

        const animationOptions = { ...defaultOptions, ...options };

        try {
            const animation = element.animate(keyframes, animationOptions);
            
            animation.addEventListener('finish', () => {
                Object.keys(keyframes).forEach(property => {
                    const values = keyframes[property];
                    const finalValue = values[values.length - 1];
                    element.style[property] = finalValue;
                });
            });

            return animation;
        } catch (error) {
            Object.keys(keyframes).forEach(property => {
                const values = keyframes[property];
                const finalValue = values[values.length - 1];
                element.style[property] = finalValue;
            });
        }
    }

    function animateTextElement(element, delay = 0) {
        // 要素が既にアニメーション済みかチェック
        if (element.dataset.animated === 'true') return;
        
        setTimeout(() => {
            element.dataset.animated = 'true';
            animateElement(element, {
                opacity: [0, 1],
                transform: ['translateY(30px)', 'translateY(0px)']
            }, {
                duration: 800,
                easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
            });
        }, delay);
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            
            if (entry.target.classList.contains('revenue-title')) {
                animateTextElement(entry.target, 0);
            } else if (entry.target.classList.contains('revenue-description')) {
                animateTextElement(entry.target, 200);
            } else if (entry.target.classList.contains('revenue-sub-description')) {
                animateTextElement(entry.target, 400);
                hasTextAnimationsExecuted = true;
            } else if (entry.target.classList.contains('revenue-flow-simple') || entry.target.classList.contains('revenue-flow-mobile')) {
                if (!hasExecutedOnce) {
                    setTimeout(() => {
                        startAnimation();
                    }, 200);
                }
            }
            
            // 要素の監視は継続（unobserveしない）
        });
    }, observerOptions);

    // DOMContentLoadedイベントで初期化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            ensureInitialState();
            initializeRevenueFlow();
            
            // ページロード後に要素をチェック
            setTimeout(() => {
                checkElementsInView();
            }, 100);
        });
    } else {
        // 既にDOMが読み込まれている場合
        ensureInitialState();
        initializeRevenueFlow();
        
        setTimeout(() => {
            checkElementsInView();
        }, 100);
    }
    
    // 初期状態でテキスト要素を非表示に
    const title = document.querySelector('.revenue-title');
    const description = document.querySelector('.revenue-description');
    const subDescription = document.querySelector('.revenue-sub-description');
    
    if (title) {
        ensureInitialState();
        observer.observe(title);
    }
    
    if (description) {
        observer.observe(description);
    }
    
    if (subDescription) {
        observer.observe(subDescription);
    }
    
    // フロー要素の監視を開始
    const flowContainer = document.querySelector('.revenue-flow-simple');
    const mobileFlowContainer = document.querySelector('.revenue-flow-mobile');
    
    if (flowContainer) {
        observer.observe(flowContainer);
    }
    
    if (mobileFlowContainer) {
        observer.observe(mobileFlowContainer);
    }
    
    // ページ表示時にもチェック（ブラウザバック等の対応）
    window.addEventListener('pageshow', (event) => {
        if (event.persisted) {
            // ブラウザのキャッシュから復元された場合
            ensureInitialState();
            setTimeout(() => {
                checkElementsInView();
            }, 100);
        }
    });
}
















// 開設までの流れセクションのアニメーション
function initSetupFlowAlternate() {
    let resizeTimer;
    
    let currentSlide = 0;
    const totalSlides = document.querySelectorAll('.carousel-item').length;
    
    const animatedElements = new WeakSet();
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const headerObserverOptions = {
        threshold: 0.15,
        rootMargin: '-50px 0px -50px 0px'
    };

    // ビューポートのサイズに応じてスケールを調整
    function adjustScale() {
        const wrapper = document.querySelector('.setup-flow-wrapper');
        const setupFlow = document.querySelector('.setup-flow-alternate');
        const viewportWidth = window.innerWidth;
        
        if (!setupFlow) return;
        
        // 769px以下または1000px以上の場合はスケール変換しない
        if (viewportWidth <= 768 || viewportWidth >= 1000) {
            setupFlow.style.transform = 'none';
            if (wrapper) wrapper.style.height = 'auto';
            return;
        }
        
        // 769px〜1000pxの間でスケール計算
        const scale = viewportWidth / 1000;
        
        setupFlow.style.transform = 'none';
        
        // 高さを計算
        requestAnimationFrame(() => {
            const originalHeight = setupFlow.scrollHeight;
            
            setupFlow.style.transform = `scale(${scale})`;
            
            const scaledHeight = originalHeight * scale;
            if (wrapper) wrapper.style.height = `${scaledHeight}px`;
            
            // 水平方向の中央配置を調整
            const originalWidth = 1000;
            const scaledWidth = originalWidth * scale;
            const leftOffset = (viewportWidth - scaledWidth) / 2;
            setupFlow.style.left = `${leftOffset}px`;
        });
    }

    // 画像の読み込みを待つ関数
    function waitForImages() {
        const images = document.querySelectorAll('.setup-flow-alternate img');
        const imagePromises = Array.from(images).map(img => {
            if (img.complete) {
                return Promise.resolve();
            }
            return new Promise(resolve => {
                img.addEventListener('load', resolve);
                img.addEventListener('error', resolve);
            });
        });
        
        return Promise.all(imagePromises);
    }

    // カルーセル機能
    function showSlide(n) {
        const container = document.getElementById('carouselContainer');
        const dots = document.querySelectorAll('.indicator-dot');
        
        if (!container) return;
        
        // スライド番号の境界チェック
        if (n >= totalSlides) {
            currentSlide = 0;
        } else if (n < 0) {
            currentSlide = totalSlides - 1;
        } else {
            currentSlide = n;
        }
        
        container.style.transform = `translateX(-${currentSlide * 100}%)`;
        
        // インジケーターの更新
        dots.forEach((dot, index) => {
            if (index === currentSlide) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });
    }
    
    function prevSlide() {
        showSlide(currentSlide - 1);
    }
    
    function nextSlide() {
        showSlide(currentSlide + 1);
    }

    // タッチスワイプ機能
    function initCarouselTouch() {
        let startX = 0;
        let startY = 0;
        let isDragging = false;
        const threshold = 50;
    
        const carousel = document.getElementById('carouselContainer');
        if (!carousel) return;
    
        carousel.addEventListener('touchstart', e => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
            isDragging = true;
        });
    
        carousel.addEventListener('touchmove', e => {
            if (!isDragging) return;
    
            const currentX = e.touches[0].clientX;
            const currentY = e.touches[0].clientY;
            const diffX = currentX - startX;
            const diffY = currentY - startY;
    
            // 横移動が縦移動より大きく、かつしきい値超えなら横スワイプとみなす
            if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > threshold) {
                e.preventDefault();
            }
        });
    
        carousel.addEventListener('touchend', e => {
            if (!isDragging) return;
    
            const endX = e.changedTouches[0].clientX;
            const diffX = endX - startX;
    
            if (diffX > threshold) {
                prevSlide();
            } else if (diffX < -threshold) {
                nextSlide();
            }
    
            isDragging = false;
        });
    }

    // ヘッダーアニメーション
    function animateHeader(header) {
        header.classList.add('animated');
        animateHeaderElements(header);
    }

    function animateHeaderElements(header) {
        const animations = [
            { selector: '.section-title', delay: 200 },
            { selector: '.section-subtitle', delay: 400 },
            { selector: '.step-badge', delay: 600 }
        ];

        animations.forEach(({ selector, delay }) => {
            const element = header.querySelector(selector);
            if (element) {
                setTimeout(() => {
                    element.style.transition = 'opacity 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94), transform 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
                    element.style.opacity = '1';
                    element.style.transform = selector === '.step-badge' ? 'scale(1)' : 'translateY(0px)';
                }, delay);
            }
        });
    }

    function handleIntersection(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }

    function handleHeaderIntersection(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting && !animatedElements.has(entry.target)) {
                animatedElements.add(entry.target);
                
                if (entry.target.classList.contains('section-header')) {
                    animateHeader(entry.target);
                }
                
                headerObserver.unobserve(entry.target);
            }
        });
    }

    const observer = new IntersectionObserver(handleIntersection, observerOptions);
    const headerObserver = new IntersectionObserver(handleHeaderIntersection, headerObserverOptions);

    function initialize() {
        const stepInfos = document.querySelectorAll('.step-info');
        stepInfos.forEach(stepInfo => {
            observer.observe(stepInfo);
        });

        const sectionHeader = document.querySelector('.setup-flow-alternate .section-header');
        if (sectionHeader) {
            sectionHeader.style.transition = 'opacity 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
            headerObserver.observe(sectionHeader);
        }

        // インジケータードットのクリックイベント設定
        const dots = document.querySelectorAll('.indicator-dot');
        dots.forEach((dot, index) => {
            dot.addEventListener('click', function() {
                showSlide(index);
            });
        });

        // 矢印ボタンのクリックイベント設定
        const prevButton = document.querySelector('.carousel-prev');
        const nextButton = document.querySelector('.carousel-next');
        
        if (prevButton) {
            prevButton.addEventListener('click', function(e) {
                e.preventDefault();
                prevSlide();
            });
        }
        
        if (nextButton) {
            nextButton.addEventListener('click', function(e) {
                e.preventDefault();
                nextSlide();
            });
        }

        initCarouselTouch();

        waitForImages().then(() => {
            adjustScale();
        });
    }

    // イベントリスナーの設定
    function setupEventListeners() {
        window.addEventListener('load', () => {
            setTimeout(adjustScale, 100);
        });

        window.addEventListener('resize', function() {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(adjustScale, 100);
        });
    }

    initialize();
    setupEventListeners();
}







// カードのアニメーション
function initRevenueCardAnimations() {
    const comparisonCards = document.querySelectorAll('.revenue-comparison-card');
    const paymentCards = document.querySelectorAll('.payment-comparison-card');
    const comparisonTitle = document.querySelector('.revenue-subtitle');
    const calculationTitle = document.querySelector('.calculation-title');
    
    const observerOptions = {
        threshold: 0.3,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                if (entry.target.classList.contains('revenue-comparison-card')) {
                    // 収益比較カードの処理
                    const card = entry.target;
                    const percentage = parseInt(card.dataset.percentage);
                    const circularProgress = card.querySelector('.circular-progress');
                    
                    // カード表示アニメーション
                    setTimeout(() => {
                        card.classList.add('visible');
                    }, index * 200);
                    
                    // 円グラフアニメーション
                    setTimeout(() => {
                        animateProgress(circularProgress, percentage);
                    }, index * 200 + 300);
                } else if (entry.target.classList.contains('payment-comparison-card')) {
                    // 決済比較カードの処理
                    const card = entry.target;
                    const pieChart = card.querySelector('.payment-pie-chart');
                    const revenuePercent = parseFloat(card.style.getPropertyValue('--revenue-percent'));
                    const feePercent = parseFloat(card.style.getPropertyValue('--fee-percent'));
                    
                    // カード表示アニメーション
                    setTimeout(() => {
                        card.classList.add('visible');
                    }, index * 150);
                    
                    // 円グラフアニメーション
                    setTimeout(() => {
                        animatePaymentPieChart(pieChart, revenuePercent, feePercent);
                    }, index * 150 + 300);
                } else {
                    showElement(entry.target);
                }
                
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // 要素を監視対象に追加
    if (comparisonTitle) {
        observer.observe(comparisonTitle);
    }
    
    if (calculationTitle) {
        observer.observe(calculationTitle);
    }
    
    comparisonCards.forEach((card, index) => {
        observer.observe(card);
    });
    
    paymentCards.forEach(card => {
        observer.observe(card);
    });
    
    // 決済カードの遅延設定
    paymentCards.forEach((card, index) => {
        const delay = index * 150;
        card.style.transitionDelay = `${delay}ms`;
    });
    
    function showElement(element) {
        element.classList.add('visible');
    }
    
    function animateProgress(element, targetPercentage) {
        let currentProgress = 0;
        const duration = 1500;
        const startTime = Date.now();
        
        function updateProgress() {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            currentProgress = targetPercentage * easeOutQuart;
            
            // CSS変数を更新して円グラフを描画
            const progressDegrees = (currentProgress / 100) * 360;
            element.style.setProperty('--progress', `${progressDegrees}deg`);
            
            if (progress < 1) {
                requestAnimationFrame(updateProgress);
            }
        }
        
        requestAnimationFrame(updateProgress);
    }
    
    function animatePaymentPieChart(element, revenuePercent, feePercent) {
        let currentRevenue = 0;
        let currentFee = 0;
        const duration = 1500;
        const startTime = Date.now();
        
        function updateProgress() {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            currentRevenue = revenuePercent * easeOutQuart;
            currentFee = feePercent * easeOutQuart;
            
            // CSS変数を更新して円グラフを描画
            const revenueDegrees = (currentRevenue / 100) * 360;
            const feeDegrees = ((currentRevenue + currentFee) / 100) * 360;
            
            element.style.background = `conic-gradient(
                #4361ee 0deg ${revenueDegrees}deg,
                #e74c3c ${revenueDegrees}deg ${feeDegrees}deg,
                #f39c12 ${feeDegrees}deg 360deg
            )`;
            
            if (progress < 1) {
                requestAnimationFrame(updateProgress);
            }
        }
        
        requestAnimationFrame(updateProgress);
    }
}






// 収益特徴セクションのスクロールアニメーション
function initFanMonetizationAnimations() {
    // アニメーション実行済みフラグ（リロードするまで保持）
    if (!window.fanMonetizationAnimationFlags) {
        window.fanMonetizationAnimationFlags = {
            titleAnimated: false,
            subtitleAnimated: false,
            imageAnimated: false,
            featuresAnimated: false
        };
    }
    
    const isMobile = window.innerWidth <= 799;
    
    const monetizationObserverOptions = isMobile ? {
        threshold: 0.1,
        rootMargin: '0px 0px 100px 0px'
    } : {
        threshold: 0.3,
        rootMargin: '0px 0px -50px 0px'
    };

    // タイトルとサブタイトルのアニメーション
    const mainTitle = document.querySelector('.fan-monetization-heading');
    const subtitle = document.querySelector('.fan-monetization-description');
    
    if (mainTitle && !window.fanMonetizationAnimationFlags.titleAnimated) {
        setTimeout(() => {
            mainTitle.style.opacity = '0';
            mainTitle.style.transform = 'translateY(20px)';
            mainTitle.style.transition = 'all 0.8s ease';
            mainTitle.style.opacity = '1';
            mainTitle.style.transform = 'translateY(0)';
            window.fanMonetizationAnimationFlags.titleAnimated = true;
        }, 200);
    }
    
    if (subtitle && !window.fanMonetizationAnimationFlags.subtitleAnimated) {
        setTimeout(() => {
            subtitle.style.opacity = '0';
            subtitle.style.transform = 'translateY(20px)';
            subtitle.style.transition = 'all 0.8s ease';
            subtitle.style.opacity = '1';
            subtitle.style.transform = 'translateY(0)';
            window.fanMonetizationAnimationFlags.subtitleAnimated = true;
        }, 400);
    }

    if (isMobile) {
        // モバイル時
        if (!window.fanMonetizationAnimationFlags.imageAnimated) {
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting && !window.fanMonetizationAnimationFlags.imageAnimated) {
                        const imageGallery = entry.target;
                        
                        setTimeout(() => {
                            imageGallery.classList.add('animate');
                            window.fanMonetizationAnimationFlags.imageAnimated = true;
                        }, 200);
                        
                        imageObserver.unobserve(imageGallery);
                        
                        setupFeatureObserver();
                    }
                });
            }, monetizationObserverOptions);

            const imageGallery = document.querySelector('.monetization-images');
            if (imageGallery && !imageGallery.classList.contains('animate')) {
                imageObserver.observe(imageGallery);
            }
        }

        // 項目部分の監視設定
        function setupFeatureObserver() {
            if (window.fanMonetizationAnimationFlags.featuresAnimated) {
                return;
            }
            
            const featureObserverOptions = {
                threshold: 0.1,
                rootMargin: '0px 0px 50px 0px'
            };
            
            const featureObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting && !window.fanMonetizationAnimationFlags.featuresAnimated) {
                        const allFeatures = document.querySelectorAll('.monetization-feature');
                        
                        // すべての項目をアニメーション
                        allFeatures.forEach(feature => {
                            const delay = parseFloat(feature.dataset.delay) * 1000;
                            setTimeout(() => {
                                feature.classList.add('animate');
                            }, delay);
                        });
                        
                        window.fanMonetizationAnimationFlags.featuresAnimated = true;
                        featureObserver.unobserve(entry.target);
                    }
                });
            }, featureObserverOptions);

            const firstFeatureItem = document.querySelector('.monetization-feature[data-delay="0.2"]');
            if (firstFeatureItem && !window.fanMonetizationAnimationFlags.featuresAnimated) {
                featureObserver.observe(firstFeatureItem);
            }
        }

    } else {
        // デスクトップ時
        if (!window.fanMonetizationAnimationFlags.featuresAnimated) {
            const monetizationObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting && !window.fanMonetizationAnimationFlags.featuresAnimated) {
                        const element = entry.target;
                        
                        if (element.classList.contains('monetization-feature') && element.dataset.delay === '0.2') {

                            const allFeatures = document.querySelectorAll('.monetization-feature');
                            allFeatures.forEach(feature => {
                                const delay = parseFloat(feature.dataset.delay) * 1000;
                                setTimeout(() => {
                                    feature.classList.add('animate');
                                }, delay);
                            });
                            
                            window.fanMonetizationAnimationFlags.featuresAnimated = true;
                            
                            if (!window.fanMonetizationAnimationFlags.imageAnimated) {
                                const imageGallery = document.querySelector('.monetization-images');
                                if (imageGallery) {
                                    setTimeout(() => {
                                        imageGallery.classList.add('animate');
                                        window.fanMonetizationAnimationFlags.imageAnimated = true;
                                    }, 800);
                                }
                            }
                            
                            monetizationObserver.unobserve(element);
                        }
                    }
                });
            }, monetizationObserverOptions);

            const firstFeatureItem = document.querySelector('.monetization-feature[data-delay="0.2"]');
            if (firstFeatureItem && !firstFeatureItem.classList.contains('animate')) {
                monetizationObserver.observe(firstFeatureItem);
            }
        }
    }
}

// ウィンドウサイズが変更された時の対応
let resizeTimer;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        initFanMonetizationAnimations();
    }, 250);
});







// アプリが開設されたらすることセクションのアニメーション
function initAfterLaunchAnimations() {
    const animationElements = [
        {
            selector: '.after-launch-title',
            initialStyles: { opacity: '0', transform: 'translateY(40px)' },
            animatedStyles: { opacity: '1', transform: 'translateY(0)' },
            delay: 200
        },
        {
            selector: '.after-launch-steps-intro',
            initialStyles: { opacity: '0', transform: 'translateY(40px)' },
            animatedStyles: { opacity: '1', transform: 'translateY(0)' },
            delay: 200
        },
        {
            selector: '.after-launch-video-container',
            initialStyles: { opacity: '0', transform: 'scale(0.98)' },
            animatedStyles: { opacity: '1', transform: 'scale(1)' },
            delay: 300
        },
        {
            selector: '.after-launch-video-cta-message',
            initialStyles: { opacity: '0', transform: 'translateY(20px)' },
            animatedStyles: { opacity: '1', transform: 'translateY(0)' },
            delay: 500
        },
        {
            selector: '.after-launch-mobile-cta-message',
            initialStyles: { opacity: '0', transform: 'translateY(20px)' },
            animatedStyles: { opacity: '1', transform: 'translateY(0)' },
            delay: 500
        }
    ];

    animationElements.forEach(item => {
        const elements = document.querySelectorAll(item.selector);
        elements.forEach(el => {
            Object.assign(el.style, {
                transition: 'opacity 1s ease-out, transform 1s ease-out',
                ...item.initialStyles
            });
        });
    });

    const stepItems = document.querySelectorAll('.after-launch-step-item');
    stepItems.forEach(item => {
        item.style.opacity = '0';
        item.style.transform = 'translateX(30px)';
        item.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    });

    const unifiedObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;

            const target = entry.target;
            
            // ステップリストが表示されたとき
            if (target.classList.contains('after-launch-steps-list')) {
                animateStepItems();
            }
            else {
                for (const config of animationElements) {
                    if (target.matches(config.selector)) {
                        setTimeout(() => {
                            Object.assign(target.style, config.animatedStyles);
                        }, config.delay);
                        break;
                    }
                }
            }
            
            // フェードイン系クラスを持つ要素の処理
            if (target.classList.contains('after-launch-fade-in') || 
                target.classList.contains('after-launch-fade-in-left') || 
                target.classList.contains('after-launch-fade-in-right')) {
                
                target.style.opacity = '1';
                if (target.classList.contains('after-launch-fade-in-left')) {
                    target.style.transform = 'translateX(0)';
                } else if (target.classList.contains('after-launch-fade-in-right')) {
                    target.style.transform = 'translateX(0)';
                } else {
                    target.style.transform = 'translateY(0)';
                }
            }
            
            // 一度処理したら監視を停止
            unifiedObserver.unobserve(target);
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    // ステップアイテムのアニメーション関数
    function animateStepItems() {
        stepItems.forEach((item, index) => {
            const delay = 0.2 * index;
            setTimeout(() => {
                item.style.opacity = '1';
                item.style.transform = 'translateX(0)';
            }, delay * 1000);
        });
    }

    // 要素を監視対象に追加
    animationElements.forEach(item => {
        document.querySelectorAll(item.selector).forEach(el => {
            unifiedObserver.observe(el);
        });
    });

    // ステップリストを監視
    const stepsSection = document.querySelector('.after-launch-steps-list');
    if (stepsSection) {
        unifiedObserver.observe(stepsSection);
    }

    // フェードイン要素を監視
    document.querySelectorAll('.after-launch-fade-in, .after-launch-fade-in-left, .after-launch-fade-in-right').forEach(el => {
        if (!el.classList.contains('after-launch-step-item')) {
            unifiedObserver.observe(el);
        }
    });

    // プレイボタンのアニメーション
    const playButton = document.querySelector('.after-launch-play-button');
    if (playButton) {
        playButton.addEventListener('click', function() {
            this.style.transform = 'translate(-50%, -50%) scale(0.9)';
            setTimeout(() => {
                this.style.transform = 'translate(-50%, -50%) scale(1)';
            }, 150);
        });
    }
}











// ヒーローセクションのアニメーション
function initHeroAnimation() {
    const hero = document.querySelector('.hero-section');
    if (!hero) return;
    
    const play = () => {
        hero.classList.remove('hero-animate-active');
        void hero.offsetWidth;
        requestAnimationFrame(() => {
            hero.classList.add('hero-animate-active');
        });
    };
    
    // 初期アニメーション
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', play);
    } else {
        play();
    }
    
    // ページキャッシュから復帰時
    window.addEventListener('pageshow', e => {
        if (e.persisted) play();
    });
    
    // タブが表示された時
    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') play();
    });
}







// 中盤CTAセクションのアニメーション
function initRevenueCTAAnimation() {
    const ctaContent = document.querySelector('.revenue-cta-content');
    const ctaVisual = document.querySelector('.revenue-cta-visual');
    
    if (!ctaContent) return;
    
    const observerOptions = {
        threshold: 0.3,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {

                const highlightText = ctaContent.querySelector('.revenue-cta-highlight');
                if (highlightText) {
                    highlightText.innerHTML = '初期費用・月額費用<span class="animated-zero">0</span>円で<br>始められます';
                }
                
                ctaContent.classList.add('visible');
                if (ctaVisual) ctaVisual.classList.add('visible');
                
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    observer.observe(ctaContent);
}






// 下部のCTAセクションのアニメーション
function initUnifiedCTAAnimation() {
    const ctaLeft = document.querySelector('.cta-split-left');
    const ctaRight = document.querySelector('.cta-split-right');
    
    if (!ctaLeft || !ctaRight) return;
    
    const observerOptions = {
        threshold: 0.3,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                ctaLeft.classList.add('visible');
                ctaRight.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    observer.observe(ctaLeft);
}