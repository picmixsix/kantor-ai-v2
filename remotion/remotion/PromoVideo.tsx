import React from "react";
import {
  AbsoluteFill,
  Img,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Series,
} from "remotion";

interface PromoProps {
  images?: string[];
  title?: string;
}

export const PromoVideo: React.FC<PromoProps> = ({
  images = [],
  title = "PRODUK REKOMENDASI",
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Durasi per gambar dalam frame
  const imageCount = images.length > 0 ? images.length : 1;
  const framesPerImage = Math.floor(durationInFrames / imageCount);

  // Animasi Teks Pop-in
  const textScale = spring({
    frame,
    fps,
    config: { damping: 12 },
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#0d0d0d", fontFamily: "sans-serif" }}>
      {images.length > 0 ? (
        <Series>
          {images.map((imgSrc, idx) => {
            return (
              <Series.Sequence key={idx} durationInFrames={framesPerImage}>
                <ImageSlide imgSrc={imgSrc} framesPerImage={framesPerImage} />
              </Series.Sequence>
            );
          })}
        </Series>
      ) : (
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
          <h2 style={{ color: "#fff" }}>Menunggu Gambar...</h2>
        </AbsoluteFill>
      )}

      {/* Dynamic Banner Teks Promo di Bagian Bawah */}
      <div
        style={{
          position: "absolute",
          bottom: 120,
          left: "5%",
          right: "5%",
          transform: `scale(${textScale})`,
          backgroundColor: "rgba(0, 0, 0, 0.85)",
          border: "3px solid #ff4757",
          padding: "30px 20px",
          borderRadius: "20px",
          textAlign: "center",
          boxShadow: "0 10px 30px rgba(0,0,0,0.5)",
        }}
      >
        <span
          style={{
            color: "#ff4757",
            fontSize: 28,
            fontWeight: "bold",
            letterSpacing: 2,
            textTransform: "uppercase",
            display: "block",
            marginBottom: 10,
          }}
        >
          SPECIAL OFFER
        </span>
        <h1
          style={{
            color: "#ffffff",
            fontSize: 48,
            fontWeight: 800,
            margin: 0,
            textShadow: "2px 2px 4px rgba(0,0,0,0.8)",
          }}
        >
          {title}
        </h1>
      </div>
    </AbsoluteFill>
  );
};

// Sub-komponen Animasi Zoom Perlahan per Gambar
const ImageSlide: React.FC<{ imgSrc: string; framesPerImage: number }> = ({
  imgSrc,
  framesPerImage,
}) => {
  const frame = useCurrentFrame();

  const scale = interpolate(frame, [0, framesPerImage], [1, 1.15], {
    extrapolateRight: "clamp",
  });

  const opacity = interpolate(
    frame,
    [0, 15, framesPerImage - 15, framesPerImage],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        opacity,
        overflow: "hidden",
      }}
    >
      <Img
        src={imgSrc}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${scale})`,
        }}
      />
    </AbsoluteFill>
  );
};
