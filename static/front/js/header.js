document.addEventListener('DOMContentLoaded', () => {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks      = document.querySelector('.nav-links');
  
    /*==============================
      1. モバイルメニュー開閉
    ==============================*/
    mobileMenuBtn?.addEventListener('click', () => {
      mobileMenuBtn.classList.toggle('active');
      navLinks.classList.toggle('active');
    });
  
    /*==============================
      2. ドロップダウン制御（複数対応）
    ==============================*/
    const isMobile = () => window.innerWidth <= 768;
  
    document.querySelectorAll('.navbar .dropdown').forEach(dropdown => {
      const link = dropdown.querySelector('.nav-link');
      const menu = dropdown.querySelector('.dropdown-menu');
      let   timeoutId = null;
      let   isMouseOver = false;
  
      /* --- PC : hover 表示 --- */
      const showMenu = () => {
        if (isMobile()) return;
        isMouseOver = true;
        clearTimeout(timeoutId);
        menu.classList.add('hover');
      };
      const hideMenu = () => {
        if (isMobile()) return;
        isMouseOver = false;
        timeoutId = setTimeout(() => {
          if (!isMouseOver) menu.classList.remove('hover');
        }, 300);
      };
  
      dropdown.addEventListener('mouseenter', showMenu);
      dropdown.addEventListener('mouseleave', hideMenu);
      menu.addEventListener('mouseenter', showMenu);
      menu.addEventListener('mouseleave', hideMenu);
  
      /* --- モバイル : タップ開閉 --- */
      link.addEventListener('click', e => {
        if (!isMobile()) return;
        e.preventDefault();
        dropdown.classList.toggle('active');
        dropdown.classList.toggle('open');
        menu.classList.toggle('hover');
      });
    });
  
    /*==============================
      3. 画面リサイズ時 初期化
    ==============================*/
    window.addEventListener('resize', () => {
      if (isMobile()) return;  /* PC→モバイルへの縮小のみ維持 */
      document.querySelectorAll('.navbar .dropdown').forEach(d => {
        d.classList.remove('active', 'open');
        d.querySelector('.dropdown-menu')?.classList.remove('hover');
      });
    });
  });