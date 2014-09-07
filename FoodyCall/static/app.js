(function(){
try {
if(localStorage.mainOrder === "undefined" || localStorage.sideOrder === "undefined") {
  localStorage.removeItem('mainOrder');
  localStorage.removeItem('sideOrder');
}

var unmask = function () {
  var s = $('.splash-input').val();
  return s.slice(1,4) + s.slice(6,9) + s.slice(10);
};

timeCheck = function () {
  var now = moment();
  var isBetween = function (m, first, second) {
    return m.isAfter(first) && m.isBefore(second);
  };
  var time = function (h, m) {
    return moment(now).hour(h).minute(m);
  };

  var weekday = parseInt(now.format('d')); //sun=0, mon=1 ..
  if(isBetween(now, time(11,30), time(14,0)) &&  weekday < 6 && weekday > 0) {
    return "Summies Lunch";
  }
  if(isBetween(now, time(17,30), time(21,0))) {
    return "Summies Dinner";
  }
  if(isBetween(now, time(21,30), time(1,0).add(1, 'd'))) {
    return "Late Night";
  }
  return "No";
};



data = [];

started = false;
//define new router class
var AppRouter = Backbone.Router.extend ({
  routes: {
    '' : function () {
      started = true;
      $('.header>div').hide();
      $('#first-header').show();
      $('.splash-container').hide();
      $('.first-container').show();
    },
    'mainOrder': function () {
      if(!started) {this.navigate('',{trigger:true});return;}
      var router = this;
      $.getJSON('/menu/' + unmask(), function (d) {
        data = d;
        console.log('Menu for user fetched.');
      });

      var searched = fuzzy.filter($('#second-header input').val(), data.map(function (i) {
        return i.item;
      })).map(function(el) {
        return _(data).findWhere({item: el.string});
      });

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
      var processed = _(searched).where({side: false});

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
        localStorage.mainOrder = t.data('id');
        router.navigate('sides', {trigger: true});
      });
    },
    'sides': function () {
      if(!started) {this.navigate('',{trigger:true});return;}
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
      var processed = _(data).where({side: true});

      itemlist.html(_.template(itemstemplate.html(), {items: processed}));
      $('.third-container .item-list .pure-g').click(function (e) {
        $('.third-container .item-list .pure-g').removeClass('selected');
        var t = $(e.currentTarget);
        t.addClass('selected');
        localStorage.sideOrder = t.data('id');
        router.navigate('special', {trigger: true});
      });
    },
    'special': function () {
      if(!started) {this.navigate('',{trigger:true});return;}
      var selectedItem = $('.third-container .item-list .pure-g.selected');
      if(selectedItem.length !== 1) {
        this.navigate('sides', {trigger: true});
      }

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
      if(!started) {this.navigate('',{trigger:true});return;}
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
      // setTimeout(cb, 2000);

        var orderedMain = _(data).findWhere({_id: localStorage.mainOrder});
        var orderedSide = _(data).findWhere({_id: localStorage.sideOrder});
        if(orderedSide.menu !== orderedMain.menu) {
          console.log('You selected items from different menus.');
          return;
        }

        var toSend = {
          destination: orderedMain.menu,
          item_id: localStorage.mainOrder,
          side_id: localStorage.sideOrder,
          special: localStorage.prevOption,
          number: unmask()
        };

        console.log(toSend);

        $.ajax({
          type: "POST",
          url: "/order",
          data: toSend,
        }).done(function( msg ) {
          console.log(msg);
          cb();
        });
    },
    'repeatLastOrder': function () {
      if(!started) {this.navigate('',{trigger:true});return;}
      if(_.isNull(localStorage.getItem('mainOrder')) || _.isNull(localStorage.getItem('sideOrder'))) {
        this.navigate('mainOrder', {trigger: true});
        return;
      }

      $('.header>div').hide();
      $('#fourth-header').show();

      $('.first-container').addClass('flip');
      setTimeout(function () {
        $('.splash-container').hide();
        $('.first-container').removeClass('flip');
        $('.fourth-container').show();
      }, 500);

      var itemstemplate = $('.fourth-container #items-template');
      var itemlist = $('.fourth-container .item-list');

      var mainOrder = _(data).findWhere({_id: localStorage.mainOrder});
      var sideOrder = _(data).findWhere({_id: localStorage.sideOrder});
      itemlist.html(_.template(itemstemplate.html(), {
        mainOrder: mainOrder.item,
        sideOrder: sideOrder.item,
        mainPrice: mainOrder.price,
        sidePrice: sideOrder.price
      }));

      var prevOption = localStorage.prevOption;
      $('textarea').val(_.isUndefined(prevOption) ? '' : prevOption);
      $('textarea').keyup(function (e) {
        localStorage.prevOption = $('textarea').val();
      });
    },
    'rate': function () {
      if(!started) {this.navigate('',{trigger:true});return;}

      var itemstemplate = $('.rate-container #items-template');
      var itemlist = $('.rate-container .item-list');

      var searched = _(fuzzy.filter($('#rate-header input').val(), data.map(function (i) {
        return i.item;
      })).map(function(el) {
        return _(data).findWhere({item: el.string});
      })).sortBy(function (i) {
        return 5 - i.rating_avg;
      });

      $('.header>div').hide();
      $('#rate-header').show();

      $('.first-container').addClass('flip');
      setTimeout(function () {
        $('.splash-container').hide();
        $('.first-container').removeClass('flip');
        $('.rate-container').show();
      }, 500);

      var router = this;
      itemlist.html(_.template(itemstemplate.html(), {items: searched}));
      $('.rate-container select.point').change(function (e) {
        var id = $(e.currentTarget).data('id');
        var pt = $(e.currentTarget).val();

        $.ajax({
          type: "POST",
          url: "/ratings",
          data: {item: id, rate: pt}
        }).done(function( msg ) {
          data = data.map(function (i) {
            if(i._id === id) {
              i.rating_avg = parseFloat(msg);
            }
            return i;
          });
          router.navigate("");
          router.navigate("rate", {trigger: true});
        });

      })
    }
  }
});


$(document).ready(function () {
  $('#first-header a').prepend('<b>' + timeCheck() + '</b> ')

  var prevTel = localStorage.prevTel;
  $('.splash-input').val(_.isUndefined(prevTel) ? '' : prevTel);
  $('.splash-input').keyup(function (e) {
    localStorage.prevTel = $('.splash-input').val();
  });
  var tel = unmask();
  var url;
  if(tel === "") {
    url = "/menu/0";
  } else {
    url = "/menu/" + unmask();
  }
  $.getJSON(url, function (d) {
    data = d;
  });

  $('#second-header input').keyup(function () {
    appRouter.navigate("");
    appRouter.navigate("mainOrder", {trigger: true});
  });

  $('#rate-header input').keyup(function () {
    appRouter.navigate("");
    appRouter.navigate("rate", {trigger: true});
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
  appRouter.navigate('#');
});

} catch(e) {
  console.log(e);
  Backbone.history.navigate('#');
}
})();
