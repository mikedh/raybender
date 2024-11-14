#include <embree3/rtcore.h>

void* create_scene(std::string config) {
    RTCDevice device = rtcNewDevice(config.c_str());
    RTCScene scene = rtcNewScene(device);
    // RTC_SCENE_FLAG_COMPACT uses less RAM by avoiding algos consuming much
    // memory and changing the acceleration structures to more compact ones.
    // RTC_SCENE_FLAG_ROBUST avoids optimizations that lower the arithmetic
    // accuracy - this solves most problems with rays passing through edges or
    // vertices.
    rtcSetSceneFlags(scene, RTC_SCENE_FLAG_COMPACT | RTC_SCENE_FLAG_ROBUST);
    return (void*)scene;
}

void release_scene(void* scene_void) {
    RTCScene scene = (RTCScene)scene_void;
    RTCDevice device = rtcGetSceneDevice(scene);
    // This releases all geometries part of the scene too.
    rtcReleaseScene(scene);
    rtcReleaseDevice(device);
}
