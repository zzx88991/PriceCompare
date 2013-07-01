// 核心函数，用于向服务器本地数据库查询商品
function search() {

    // 生成排序参数
    var sort;
    if (window['sort'] == '价格（升序）')
        sort = 'price';
    else if (window['sort'] == '价格（降序）')
        sort = '-price';
    else
        sort = 'name';

    // 生成站点来源参数
    var site = $(".tab-pane.active").attr("id");

    $(".tab-pane.active").load(
        "/ajax/search/",
        {
            search_query: window['search_query'],
            num: window['num'],
            price_low: window['price_low'],
            price_high: window['price_high'],
            check_fav: window['check_fav'],
            sort: sort,
            site: site
        },
        function (data) {
            $(this).html(data);

            $('.carousel').carousel();

            // 监控收藏图标
            $('.icon-fav').click(function(){

                item_id = $(this).attr('item-id');


                $.post(
                    "/ajax/favorite/",
                    {item_id: item_id},
                    function(json){
                        $('em[item-id='+item_id+']').text(json.fav_num + '人收藏');
                        if(json.is_fav){
                            $('.thumbnail[item-id='+item_id+']').addClass('alert-success');
                        }
                        else{
                            $('.thumbnail[item-id='+item_id+']').removeClass('alert-success');
                        }
                    },
                    'json'
                );
            });
        });

}

//用于检索互联网以更新数据库
function update() {

    // 提示用户正在更新
    var msg = $.globalMessenger().post({
        message: '您看到的是目前我们本地数据库里的商品信息，后台正在努力为您检索最新的相关商品，请耐心等待，谢谢！',
        type: 'info',
        showCloseButton: true,
        actions: {
            confirm: {
                label: '好的',
                action: function () {
                    msg.hide();
                }
            }

        }
    });

    $.post(
        "/ajax/update/",
        {
            search_query: window['search_query'],
            search_page: window['search_page']

        },
        function (data, status, xhr) {
            // 如果返回222,表示更新完毕，再次执行搜索
            if (xhr.status == '222') {
                // 弹出提示窗口
                var msg = $.globalMessenger().post({
                    message: '您所检索的商品信息已更新，是否立即重新搜索？',
                    type: 'success',
                    showCloseButton: true,
                    actions: {
                        confirm: {
                            label: '确定',
                            action: function () {
                                search();
                                $('#more-div').show();
                                msg.hide();
                            }
                        },

                        cancel: {
                            label: '取消',
                            action: function () {
                                msg.hide();
                            }
                        }

                    }
                });
            }


        }
    );


}
