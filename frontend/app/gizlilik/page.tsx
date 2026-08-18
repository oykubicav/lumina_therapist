import PageShell, { Block } from "@/components/PageShell";

export const metadata = {
  title: "Gizlilik ve veriler",
  description:
    "Neva hangi verileri tutuyor, ne kadar süreyle saklıyor ve nasıl siliniyor.",
};

export default function GizlilikPage() {
  return (
    <PageShell
      title="Gizlilik ve veriler"
      intro="Ruh sağlığıyla ilgili konuştuğun bir yerde neyin saklandığını bilmek hakkın. Kısa ve açık anlatalım."
    >
      <Block heading="Üyelik zorunlu değil">
        <p>
          Neva&apos;yı hesap açmadan kullanabilirsin. Bu durumda kimliğinle
          ilişkilendirilebilecek hiçbir bilgi istenmiyor; oturumun tarayıcında
          tutulan geçici bir kimlikle yürüyor.
        </p>
      </Block>

      <Block heading="Mesajların">
        <p>
          Yazdığın mesajların ham hâli kalıcı olarak saklanmıyor. Sohbetin
          tutarlı ilerleyebilmesi için oturum süresince geçici olarak tutuluyor,
          sonrasında siliniyor.
        </p>
        <p>
          Sistem kayıtlarına mesaj içeriği yazılmıyor. Kayıtlarda yalnızca
          teknik bilgiler bulunuyor: isteğin ne kadar sürdüğü, hangi konu
          başlığında arama yapıldığı, kalite kontrolünden geçip geçmediği.
        </p>
      </Block>

      <Block heading="Hesap açarsan">
        <p>
          Hesap açtığında e-posta adresin ve şifrenin şifrelenmiş özeti
          saklanıyor. Şifrenin kendisi hiçbir yerde açık biçimde tutulmuyor.
        </p>
        <p>
          Ölçüm yaptıysan sonuçların hesabınla ilişkilendiriliyor — zaman
          içindeki değişimi görebilmen için. Bu veriyi istediğin an
          silebilirsin.
        </p>
      </Block>

      <Block heading="Silme hakkı">
        <p>
          Sohbet ekranındaki çöp kutusu simgesiyle oturumunu ve mesajlarını
          anında silebilirsin.
        </p>
        <p>
          Hesabını silmek istersen, hesabına bağlı her şey — oturumlar,
          mesajlar, ölçüm sonuçları — birlikte siliniyor. Bu işlem geri
          alınamıyor.
        </p>
      </Block>

      <Block heading="Nerede tutuluyor">
        <p>
          Veriler Avrupa Birliği sınırları içindeki sunucularda (Frankfurt)
          barındırılıyor. Yapay zekâ cevaplarının üretimi için Anthropic
          altyapısı kullanılıyor; bu sağlayıcıya gönderilen içerik model
          eğitiminde kullanılmıyor.
        </p>
      </Block>

      <Block heading="Yapay zekâ olduğu açıkça belirtilir">
        <p>
          Neva bir yapay zekâ sistemidir ve bunu hiçbir noktada gizlemez.
          İnsan bir uzman olduğu izlenimi vermez. Her cevabın nasıl üretildiğini
          inceleyebilmen için şeffaflık paneli sunar. Bu yaklaşım Avrupa Birliği
          Yapay Zekâ Yasası&apos;nın şeffaflık ilkeleriyle uyumludur.
        </p>
      </Block>
    </PageShell>
  );
}
