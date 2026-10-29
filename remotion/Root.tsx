import React from "react";
import { Composition } from "remotion";
import { PromoVideo } from "./PromoVideo";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="PromoVideo"
        component={PromoVideo}
        durationInFrames={1800} // 60 detik (30 fps * 60 detik)
        fps={30}
        width={1080}
        height={1920} // Format Portrait / Shorts 9:16
        defaultProps={{
          images: [],
          title: "PRODUK UNGGULAN",
        }}
      />
    </>
  );
};
