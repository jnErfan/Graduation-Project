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

  const showPageAnimation = () => {
    document.querySelectorAll('.page-animation').forEach((element) => {
      element.classList.add('show');
    });
  };

  if (document.readyState === 'complete') {
    window.clearTimeout(preloaderTimer);
    hidePreloader();
    showPageAnimation();
  }

  window.addEventListener('load', () => {
    window.clearTimeout(preloaderTimer);
    hidePreloader();
    showPageAnimation();
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

  // Counter animation function
  function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const end = parseInt(target.replace(/[^\d]/g, ''));
    const startTime = performance.now();
    const suffix = target.replace(/[\d]/g, ''); // Extract non-numeric suffix like '%'

    function updateCounter(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Easing function for smooth animation
      const easeOutQuart = 1 - Math.pow(1 - progress, 4);
      const current = Math.floor(start + (end - start) * easeOutQuart);
      
      element.textContent = current.toLocaleString() + suffix;
      
      if (progress < 1) {
        requestAnimationFrame(updateCounter);
      } else {
        element.textContent = target;
      }
    }
    
    requestAnimationFrame(updateCounter);
  }

  // Initialize counter animations when they come into view
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const counters = entry.target.querySelectorAll('.counter-number');
        counters.forEach(counter => {
          const target = counter.getAttribute('data-target');
          if (target && !counter.classList.contains('animated')) {
            counter.classList.add('animated');
            animateCounter(counter, target);
          }
        });
        counterObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3 });

  // Observe elements containing counters
  document.querySelectorAll('.stats-row, .stagger-container').forEach(container => {
    counterObserver.observe(container);
  });

  // Stagger animation for elements
  const staggerObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const staggerItems = entry.target.querySelectorAll('.stagger-item');
        staggerItems.forEach((item, index) => {
          setTimeout(() => {
            item.classList.add('show');
          }, index * 150); // 150ms delay between each item
        });
        staggerObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });

  // Observe stagger containers
  document.querySelectorAll('.stagger-container').forEach(container => {
    staggerObserver.observe(container);
  });

  const revealTargets = document.querySelectorAll(
    'section, .navbar, footer, .card, .info-box, .stats-card, .event-card, .contact-card, .metric-card, .program-card, .testimonial-card, .story-card, .story-image-card, .hero-banner img, .hero-badge, .event-strip, .section-title'
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
});
