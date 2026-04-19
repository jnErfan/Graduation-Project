document.addEventListener('DOMContentLoaded', function () {
  const alertNode = document.querySelector('.alert');
  if (alertNode) {
    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(alertNode);
      bsAlert.close();
    }, 5000);
  }

  document.body.classList.add('js-enabled');

  const preloader = document.getElementById('site-preloader');
  const hidePreloader = () => {
    if (!preloader) return;
    preloader.classList.add('site-preloader-hidden');
    window.setTimeout(() => {
      preloader.remove();
    }, 500);
  };

  const preloaderTimer = window.setTimeout(hidePreloader, 5000);

  if (document.readyState === 'complete') {
    window.clearTimeout(preloaderTimer);
    hidePreloader();
  }

  window.addEventListener('load', () => {
    window.clearTimeout(preloaderTimer);
    hidePreloader();
  });

  const translationButton = document.getElementById('translation-toggle');
  const translationMap = {
    'Home': '首页',
    'About': '关于',
    'About us': '关于我们',
    'Admissions': '招生',
    'Academics': '学术',
    'Faculty': '教师',
    'Students Life': '学生生活',
    'Alumni': '校友',
    'News': '新闻',
    'Events': '活动',
    'Contact': '联系',
    'Login': '登录',
    'Apply Now': '立即申请',
    'Contact Us': '联系我们',
    'Read More News': '阅读更多新闻',
    'Learn More': '了解更多',
    'Subscribe': '订阅',
    'Email address': '电子邮件地址',
    'Useful Links': '有用链接',
    'Quick Links': '快速链接',
    'Newsletter': '新闻订阅',
    'Jiangsu Vocational College of Agriculture and Forestry': '江苏农业职业技术学院',
    'Study in China with JSAFC': '与JSAFC一起在中国学习',
    'The School of International Education at Jiangsu Vocational College of Agriculture and Forestry welcomes international students with high-quality vocational programs, scholarships, and global exchange opportunities.': '江苏农业职业技术学院国际教育学院欢迎国际学生，提供高质量的职业项目、奖学金和全球交流机会。',
    '1': '1',
    '2': '2',
    '3': '3',
    '8': '8',
    '65+': '65+',
    '250+': '250+',
    'Top 20': '前20名',
    'Campuses': '校区',
    'Countries represented': '代表国家',
    'Awards received': '获奖',
    'International Awards': '国际奖项',
    'Campus Landscape': '校园风景',
    'Featured Programs': '特色专业',
    'Student Testimonials': '学生推荐',
    'Our Mission': '我们的使命',
    'Our Vision': '我们的愿景',
    'Latest News': '最新新闻',
    'Admissions and campus updates': '招生与校园更新',
    'Spring Semester Open House': '春季学期开放日',
    'Join us to explore campus facilities, meet our faculty, and learn about scholarship opportunities.': '加入我们，参观校园设施，见见我们的教师，并了解奖学金机会。',
    'RSVP Now': '立即预约',
    'Starts in 3 weeks': '三周后开始',
    'Innovative Curriculum': '创新课程',
    'Modern Facilities': '现代化设施',
    'Expert Faculty': '专家教师',
    'Innovative Curriculum': '创新课程',
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eget lacus id tortor facilisis.': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eget lacus id tortor facilisis.',
    'Donec gravida risus at sollicitudin luctus. Nullam feugiat odio vitae justo pharetra.': 'Donec gravida risus at sollicitudin luctus. Nullam feugiat odio vitae justo pharetra.',
    'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae.': 'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae.',
    'Our Story': '我们的故事',
    'Educating Minds, Inspiring Hearts': '启迪心智，激励心灵',
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas vitae odio ac nisi tristique venenatis. Nullam feugiat ipsum vitae justo finibus, in sagittis dolor malesuada. Aenean vel fringilla est, a vulputate massa.': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas vitae odio ac nisi tristique venenatis. Nullam feugiat ipsum vitae justo finibus, in sagittis dolor malesuada. Aenean vel fringilla est, a vulputate massa.',
    '1965': '1965',
    '1982': '1982',
    '1998': '1998',
    '2010': '2010',
    'Etiam at tincidunt arcu. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.': 'Etiam at tincidunt arcu. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.',
    'Donec dignissim, odio ac imperdiet luctus, ante nisl accumsan justo, nec tempus augue mi in nulla.': 'Donec dignissim, odio ac imperdiet luctus, ante nisl accumsan justo, nec tempus augue mi in nulla.',
    'Suspendisse potenti. Nullam lacinia dictum auctor. Phasellus euismod sem at dui imperdiet, ac tincidunt mi placerat.': 'Suspendisse potenti. Nullam lacinia dictum auctor. Phasellus euismod sem at dui imperdiet, ac tincidunt mi placerat.',
    'Vestibulum ultrices magna ut faucibus sollicitudin. Sed eget venenatis enim, nec imperdiet ex.': 'Vestibulum ultrices magna ut faucibus sollicitudin. Sed eget venenatis enim, nec imperdiet ex.',
    'Campus life': '校园生活',
    'Campus walkway': '校园通道',
    'International Student Life': '国际学生生活',
    'Join a diverse student community with activities, cultural exchange opportunities, and academic support.': '加入多元化的学生社区，参与活动、文化交流机会和学术支持。',
    'Experience the JSAFC campus through our international education programs and student support services.': '通过我们的国际教育项目和学生支持服务体验JSAFC校园。',
    'Jiangsu Vocational College of Agriculture and Forestry': '江苏农业职业技术学院',
    'All Rights Reserved.': '版权所有。'
  };
  const reverseTranslationMap = Object.fromEntries(Object.entries(translationMap).map(([key, value]) => [value, key]));

  function translateTextNodes(map) {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        if (!node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        const parentTag = node.parentElement?.tagName;
        if (['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEXTAREA', 'OPTION'].includes(parentTag)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });

    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (!node._originalText) node._originalText = node.nodeValue;
      const originalText = node._originalText;
      const trimmedText = originalText.trim();
      if (map[trimmedText]) {
        node.nodeValue = originalText.replace(trimmedText, map[trimmedText]);
      } else {
        node.nodeValue = originalText;
      }
    }
  }

  function translateInputs(map) {
    document.querySelectorAll('[placeholder]').forEach((input) => {
      const original = input.dataset.originalPlaceholder || input.placeholder;
      if (!input.dataset.originalPlaceholder) input.dataset.originalPlaceholder = original;
      input.placeholder = map[original] || original;
    });
  }

  function setLanguage(lang) {
    const map = lang === 'zh' ? translationMap : reverseTranslationMap;
    translateTextNodes(map);
    translateInputs(map);
    document.documentElement.lang = lang === 'zh' ? 'zh' : 'en';
    translationButton.textContent = lang === 'zh' ? '中' : 'EN';
    translationButton.classList.toggle('active', lang === 'zh');
    localStorage.setItem('siteLanguage', lang);
  }

  translationButton.addEventListener('click', () => {
    const currentLang = localStorage.getItem('siteLanguage') === 'zh' ? 'en' : 'zh';
    setLanguage(currentLang);
  });

  const savedLanguage = localStorage.getItem('siteLanguage') || 'en';
  setLanguage(savedLanguage);

  const revealTargets = document.querySelectorAll(
    'section, .card, .info-box, .stats-card, .event-card, .contact-card, .hero-banner img, .section-title'
  );

  if ('IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('show');
            observer.unobserve(entry.target);
          }
        });
      },
      {
        threshold: 0.15,
        rootMargin: '0px 0px -90px 0px',
      }
    );

    revealTargets.forEach((target) => {
      target.classList.add('scroll-reveal');
      revealObserver.observe(target);
    });
  } else {
    revealTargets.forEach((target) => {
      target.classList.add('show');
    });
  }

  // ===== ADVANCED ANIMATIONS =====

  // Number Counter Animation
  function animateCounter(element, target, duration = 2000) {
    const start = parseInt(element.textContent) || 0;
    const increment = (target - start) / (duration / 16);
    let current = start;

    element.classList.add('counting');

    const timer = setInterval(() => {
      current += increment;
      if ((increment > 0 && current >= target) || (increment < 0 && current <= target)) {
        element.textContent = target.toLocaleString();
        element.classList.remove('counting');
        clearInterval(timer);
      } else {
        element.textContent = Math.floor(current).toLocaleString();
      }
    }, 16);
  }

  // Initialize counter animations
  function initCounters() {
    const counters = document.querySelectorAll('.counter-number');

    if ('IntersectionObserver' in window) {
      const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !entry.target.hasAttribute('data-animated')) {
            entry.target.setAttribute('data-animated', 'true');
            const target = parseInt(entry.target.getAttribute('data-target')) || 0;
            animateCounter(entry.target, target);
          }
        });
      }, { threshold: 0.5 });

      counters.forEach((counter) => {
        counterObserver.observe(counter);
      });
    } else {
      // Fallback for browsers without IntersectionObserver
      counters.forEach((counter) => {
        const target = parseInt(counter.getAttribute('data-target')) || 0;
        animateCounter(counter, target);
      });
    }
  }

  // Staggered animations for lists
  function initStaggeredAnimations() {
    const staggerContainers = document.querySelectorAll('.stagger-container');

    staggerContainers.forEach((container) => {
      const items = container.querySelectorAll('.stagger-item');

      if ('IntersectionObserver' in window) {
        const staggerObserver = new IntersectionObserver((entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              items.forEach((item, index) => {
                setTimeout(() => {
                  item.classList.add('show');
                }, index * 100);
              });
              staggerObserver.unobserve(entry.target);
            }
          });
        }, { threshold: 0.3 });

        staggerObserver.observe(container);
      } else {
        items.forEach((item, index) => {
          setTimeout(() => {
            item.classList.add('show');
          }, index * 100);
        });
      }
    });
  }

  // Advanced scroll animations with different effects
  function initAdvancedScrollAnimations() {
    const animatedElements = document.querySelectorAll('[data-animation]');

    if ('IntersectionObserver' in window) {
      const animationObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const animationType = entry.target.getAttribute('data-animation');
            const delay = entry.target.getAttribute('data-delay') || 0;

            setTimeout(() => {
              entry.target.classList.add(`${animationType}-animation`);
            }, delay);

            animationObserver.unobserve(entry.target);
          }
        });
      }, { threshold: 0.2 });

      animatedElements.forEach((element) => {
        animationObserver.observe(element);
      });
    }
  }

  // Magnetic hover effect
  function initMagneticEffect() {
    const magneticElements = document.querySelectorAll('.magnetic');

    magneticElements.forEach((element) => {
      element.addEventListener('mousemove', (e) => {
        const rect = element.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;

        element.style.transform = `translate(${x * 0.1}px, ${y * 0.1}px)`;
      });

      element.addEventListener('mouseleave', () => {
        element.style.transform = 'translate(0px, 0px)';
      });
    });
  }

  // Typing animation
  function initTypingAnimation() {
    const typingElements = document.querySelectorAll('.typing-text');

    typingElements.forEach((element) => {
      const text = element.textContent;
      element.textContent = '';
      element.classList.add('typing-animation');

      let i = 0;
      const timer = setInterval(() => {
        if (i < text.length) {
          element.textContent += text.charAt(i);
          i++;
        } else {
          clearInterval(timer);
          element.classList.remove('typing-animation');
        }
      }, 100);
    });
  }

  // Progress bar animations
  function initProgressBars() {
    const progressBars = document.querySelectorAll('.progress-animated');

    progressBars.forEach((bar) => {
      const width = bar.getAttribute('data-width') || '75%';
      bar.style.setProperty('--progress-width', width);
      bar.classList.add('progress-fill');
    });
  }

  // Particle effect
  function createParticles() {
    const particleContainers = document.querySelectorAll('.particle-container');

    particleContainers.forEach((container) => {
      for (let i = 0; i < 5; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.animationDelay = `${Math.random() * 3}s`;
        container.appendChild(particle);
      }
    });
  }

  // Enhanced hover effects
  function initEnhancedHovers() {
    const hoverElements = document.querySelectorAll('.hover-lift, .hover-rotate, .hover-scale');

    hoverElements.forEach((element) => {
      element.addEventListener('mouseenter', () => {
        element.style.zIndex = '10';
      });

      element.addEventListener('mouseleave', () => {
        element.style.zIndex = 'auto';
      });
    });
  }

  // Morphing animations
  function initMorphingElements() {
    const morphElements = document.querySelectorAll('.morph-trigger');

    morphElements.forEach((element) => {
      element.addEventListener('click', () => {
        const target = document.querySelector(element.getAttribute('data-target'));
        if (target) {
          target.classList.add('morph-animation');
          setTimeout(() => {
            target.classList.remove('morph-animation');
          }, 4000);
        }
      });
    });
  }

  // Initialize all advanced animations
  initCounters();
  initStaggeredAnimations();
  initAdvancedScrollAnimations();
  initMagneticEffect();
  initTypingAnimation();
  initProgressBars();
  createParticles();
  initEnhancedHovers();
  initMorphingElements();

  // Performance optimization - reduce animations on low-power devices
  if ('deviceMemory' in navigator && navigator.deviceMemory < 4) {
    document.documentElement.classList.add('reduced-motion');
  }

  // Add loading states
  const buttons = document.querySelectorAll('.btn');
  buttons.forEach((button) => {
    button.addEventListener('click', function() {
      if (this.form && !this.form.checkValidity()) return;

      const originalText = this.innerHTML;
      this.innerHTML = '<span class="loading-dots"><span></span><span></span><span></span></span>';
      this.disabled = true;

      setTimeout(() => {
        this.innerHTML = originalText;
        this.disabled = false;
      }, 2000);
    });
  });

});
