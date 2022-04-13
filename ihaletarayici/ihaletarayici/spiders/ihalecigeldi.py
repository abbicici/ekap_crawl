import scrapy
from scrapy_splash import SplashRequest

class IhalecigeldiSpider(scrapy.Spider):
    name = 'ihalecigeldi'
    allowed_domains = ['ekap.kik.gov.tr']
    
    script='''
        function main(splash, args)
            splash.private_mode_enabled=false
            assert(splash:go(args.url))
            assert(splash:wait(1))
            mal_box=assert(splash:select_all('.custom-control-input'))
            mal_box[1]:mouse_click()
            sehir=assert(splash:select('[title="İhalenin yapıldığı il"]'))
            sehir:send_text("malatya")
            assert(splash:wait(1))
            splash:set_viewport_full()
            flt_box=assert(splash:select('.btn-block'))
            flt_box:mouse_click()
            assert(splash:wait(1))
            return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(url='https://ekap.kik.gov.tr/EKAP/Ortak/IhaleArama/index.html',callback=self.parse,endpoint="execute",args={
            'lua_source':self.script
        })

    def parse(self, response):
        for listem in response.xpath("/html/body/div/div[2]/div/div[2]/div"):

            yield{
                "ihale No":    listem.xpath(".//div/div/div/div/div/div/div/h6/text()").get(),
                "Açıklama":    listem.xpath(".//div/div/div/div[2]/div/div/p[1]/text()").get(),
                "il ve Tarih": listem.xpath(".//div/div/div/div[2]/div/div/p[2]/text()").get(),
                "İdare":       listem.xpath(".//div/div/div/div[3]/div/div/p/text()").get()
            }