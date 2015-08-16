# old-python-game-fwk

Фреймворк для написания игр на python-е. Создан специально для разработки игр в рамках омского Ludum Dare, однако, может быть использован где угодно, кем угодно на свой страх и риск (да да, мне тоже страшновато).

### Об используемых технологиях

Фреймворк использует библиотеку [pyglet](http://www.pyglet.org/), что позволяет работать с графикой, звуком и устройствами ввода. Кое-где напрямую используется OpenGL.

Звуки, хранящиеся в сжатых форматах не работают если в системе не установлена библиотека AVbin.

### Об архитектуре

Фреймворк добавляет несколько более высокоуровневых абстракций:

* Экран (Screen) - в каждый момент времени активен ровно один экран. Активный экран определяет, что рисуется в окне игры, а так же обрабатывает события ввода. Каждый экран состоит из одного или нескольких слоёв. Слои отрисовываются в том порядке, в котором они были добавлены к экрану.
* Слой (Layer) - может рисовать в окне задний фон, игровой мир или какой-нибудь элемент управления. Каждый слой получает сообщения о событиях от экрана.
* Игра (Game) - игровой мир с сущностями и правилами их изменения и отображения.
* Игровая сущность (GameEntity) - объект, существующий в игровом мире с координатами и прочими плюшками. Может отображаться как спрайт (SpriteGameEntity) или спрайт с анимацией (AnimatedGameEntity), или как-нибудь ещё - можно переопределить метод draw().

### Об использовании этого репозитория

~~Проекты игр будут находиться в отдельных репозиториях, форкнутых от этого.~~ Идея оказалась не самой удачной. Теперь папка фреймворка вынесена в отдельный репозиторий, который может быть подключен при помощи замечательного [GIT submodules](https://git-scm.com/book/ru/v1/Инструменты-Git-Подмодули).

**Это важно:** фреймворк должен находиться в каталоге (модуле) ```fwk```. Это связано с нечеловеческим количеством импортов по абсолютному пути на ранних этапах разработки и ленью на текущем.
