try {

data = [];

$.getJSON('http://127.0.0.1:3000/menu', function (d) {
  data = d;
});

//define new router class
var AppRouter = Backbone.Router.extend ({
  routes: {
    '' : function () {
      $('.header>div').hide();
      $('#first-header').show();
      $('.splash-container').hide();
      $('.first-container').show();
    },
    'mainOrder': function () {
      var router = this;
      var num = $('.splash-input').val();

      if(num.length !== 14) {
        this.navigate("", {trigger: true});
        return;
      }
      num = num.match(/\d/g).join("");

      $('.second-container').show();
      $('.header>div').hide();
      $('#second-header').show();

      $('.first-container').addClass('flip');
      setTimeout(function () {
        $('.first-container').hide();
        $('.first-container').removeClass('flip');
      }, 500);

      var itemstemplate = $('.second-container #items-template');
      var itemlist = $('.second-container .item-list');
      var processed = _(data).where({side: false}).map(function (i) {
        i.prev = 0;
        i.rating_avg = (Math.random() * 4 | 0) + 1.5;
        return i;
      });

      var switcher = $('.foody-switcher span').text();

      var filters = [];
      if($('.vegan').hasClass('foody-checked')){
        filters.push("vegan");
      }
      if($('.gluten-free').hasClass('foody-checked')){
        filters.push("gluten-free");
      }
      //Filters
      processed = processed.filter(function (i) {
        return _.isEqual(filters, _.intersection(filters, i.filter));
      });

      //Sorting
      processed = _(processed).sortBy(function (i) {
        if(switcher === "Cheapest") {
          return i.price;
        }
        if(switcher === "Prev Orders") {
          return i.prev;
        }
        return 5 - i.rating_avg;
      });
      itemlist.html(_.template(itemstemplate.html(), {items: processed}));
      $('.second-container .item-list .pure-g').click(function (e) {
        $('.second-container .item-list .pure-g').removeClass('selected');
        var t = $(e.currentTarget);
        t.addClass('selected');
        router.navigate('sides', {trigger: true});
      });
    },
    'sides': function () {
      var router = this;
      var selectedItem = $('.second-container .item-list .pure-g.selected');
      if(selectedItem.length !== 1) {
        this.navigate('mainOrder', {trigger: true});
      }
      $('#third-header .pure-menu-heading').html('Sides for <b>' + selectedItem.find('h3').text() + '</b>');

      $('.header>div').hide();
      $('#third-header').show();

      $('.second-container').addClass('flip');
      setTimeout(function () {
        $('.splash-container').hide();
        $('.second-container').removeClass('flip');
        $('.third-container').show();
      }, 500);

      var itemstemplate = $('.third-container #items-template');
      var itemlist = $('.third-container .item-list');
      var processed = _(data).where({side: true}).map(function (i) {
        i.prev = 0;
        i.rating_avg = (Math.random() * 4 | 0) + 1.5;
        return i;
      });

      itemlist.html(_.template(itemstemplate.html(), {items: processed}));
      $('.third-container .item-list .pure-g').click(function (e) {
        $('.third-container .item-list .pure-g').removeClass('selected');
        var t = $(e.currentTarget);
        t.addClass('selected');
        router.navigate('special', {trigger: true});
      });
    },
    'special': function () {
      var selectedItem = $('.third-container .item-list .pure-g.selected');
      if(selectedItem.length !== 1) {
        this.navigate('sides', {trigger: true});
      }
      // $('#fourth-header .pure-menu-heading').html('Sides for <b>' + selectedItem.find('h3').text() + '</b>');

      $('.header>div').hide();
      $('#fourth-header').show();

      $('.third-container').addClass('flip');
      setTimeout(function () {
        $('.splash-container').hide();
        $('.third-container').removeClass('flip');
        $('.fourth-container').show();
      }, 500);

      var itemstemplate = $('.fourth-container #items-template');
      var itemlist = $('.fourth-container .item-list');

      var mainOrder = $('.second-container .item-list .pure-g.selected');
      var sideOrder = $('.third-container .item-list .pure-g.selected');
      if(mainOrder.length < 1 || sideOrder.length < 1) {
        this.navigate('', {trigger: true});
      }
      itemlist.html(_.template(itemstemplate.html(), {
        mainOrder: mainOrder.find('h3').text(),
        sideOrder: sideOrder.find('h3').text(),
        mainPrice: parseFloat(mainOrder.data('price')),
        sidePrice: parseFloat(sideOrder.data('price'))
      }));

      var prevOption = localStorage.prevOption;
      $('textarea').val(_.isUndefined(prevOption) ? '' : prevOption);
      $('textarea').keyup(function (e) {
        localStorage.prevOption = $('textarea').val();
      });


    },
    sending: function () {
      $('.header>div').hide();
      $('#first-header').show();

      $('.fourth-container').addClass('flip');
      setTimeout(function () {
        $('.splash-container').hide();
        $('.fourth-container').removeClass('flip');
        $('.fifth-container').show();
      }, 500);
      console.log("sending");
      var cb = function () {
        $('.sending').hide();
        $('.sent').show();
        $('.fifth-container p').show();
      };
      setTimeout(cb, 2000);
    }
  }
});


$(document).ready(function () {
  var prevTel = localStorage.prevTel;
  $('.splash-input').val(_.isUndefined(prevTel) ? '' : prevTel);
  $('.splash-input').keyup(function (e) {
    localStorage.prevTel = $('.splash-input').val();
  });

  $('.foody-checkbox').click(function (e) {
    var t = $(e.currentTarget);
    t.toggleClass("foody-checked");
    t.find('.fa').toggleClass('fa-check-square-o');
    t.find('.fa').toggleClass('fa-square-o');

    appRouter.navigate("");
    appRouter.navigate("mainOrder", {trigger: true});
  });

  $('.foody-switcher').click(function (e) {
    var t = $(e.currentTarget);
    var content = ["Best Rated", "Cheapest", "Prev Orders"];
    var current = t.find('span').text();
    current = content.indexOf(current);
    if(current === 2) {
      current = -1;
    }
    var next = content[current + 1];
    t.find('span').text(next);

    appRouter.navigate("");
    appRouter.navigate("mainOrder", {trigger: true});
  });


  var appRouter = new AppRouter();
  Backbone.history.start();
  Backbone.history.navigate('#');
});

} catch(e) {
  console.log(e);
  Backbone.history.navigate('#');
}
