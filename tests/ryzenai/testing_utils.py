# Copyright 2023 The HuggingFace Team. All rights reserved.
# Licensed under the MIT License.

import json
import os

from transformers import set_seed


SEED = 42

BASELINE_JSON = ".\\tests\\ryzenai\\operators_baseline.json"  # For RyzenSDK 1.0.1

DEFAULT_CACHE_DIR = "ryzen_cache"
DEFAULT_VAIP_CONFIG = ".\\tests\\ryzenai\\vaip_config.json"


def parse_json(json_path):
    with open(json_path, "r") as json_file:
        data = json.load(json_file)
        result = {"all": 0, "dpu": 0, "cpu": 0}
        for entry in data["deviceStat"]:
            result[entry["name"].lower()] = entry["nodeNum"]
        return result


class RyzenAITestCaseMixin:
    def run_model(
        self,
        model_class,
        model_id,
        ort_input,
        use_cpu_runner,
        compile_reserve_const_data,
        vaip_config,
        cache_dir=None,
        cache_key=None,
        file_name=None,
    ):
        os.environ["XLNX_ENABLE_CACHE"] = "0"
        os.environ["XLNX_USE_SHARED_CONTEXT"] = "1"
        os.environ["USE_CPU_RUNNER"] = "1" if use_cpu_runner else "0"
        os.environ["VAIP_COMPILE_RESERVE_CONST_DATA"] = "1" if compile_reserve_const_data else "0"

        provider_options = {}
        if cache_dir:
            provider_options["cacheDir"] = cache_dir
        if cache_key:
            provider_options["cacheKey"] = cache_key

        model_instance = model_class.from_pretrained(
            model_id, file_name=file_name, vaip_config=vaip_config, provider_options=provider_options
        )

        if isinstance(ort_input, dict):
            outputs = model_instance(**ort_input)
        else:
            outputs = model_instance(ort_input)

        return outputs

    def prepare_outputs(
        self, model_id, model_class, ort_input, vaip_config, cache_dir=None, cache_key=None, file_name=None
    ):
        set_seed(SEED)
        output_ipu = self.run_model(
            model_class,
            model_id,
            ort_input,
            use_cpu_runner=0,
            compile_reserve_const_data=0,
            vaip_config=vaip_config,
            cache_dir=cache_dir,
            cache_key=cache_key,
            file_name=file_name,
        )

        output_cpu = self.run_model(
            model_class,
            model_id,
            ort_input,
            use_cpu_runner=1,
            compile_reserve_const_data=1,
            vaip_config=vaip_config,
            file_name=file_name,
        )

        return output_ipu, output_cpu

    def get_ops(self, cache_dir, cache_key):
        result = parse_json(os.path.join(cache_dir, cache_key, "vitisai_ep_report.json"))
        return result

    def get_baseline_ops(self, key):
        with open(BASELINE_JSON, "r") as json_file:
            data = json.load(json_file)
            return data[key]


RYZEN_PREQUANTIZED_MODEL_IMAGE_CLASSIFICATION = [
    "amd/efficientnet-es",
    "amd/ese_vovnet39b",
    "amd/inception_v4",
    "amd/mnasnet_b1",
    "amd/mobilenet_v2_1.0_224",
    "amd/resnet50",
    "amd/squeezenet",
]


RYZEN_PREQUANTIZED_MODEL_OBJECT_DETECTION = [
    "amd/retinaface",
    "amd/yolov3",
    "amd/yolov5s",
    "amd/yolov8m",
    "amd/yolox-s",
]

RYZEN_PREQUANTIZED_MODEL_IMAGE_SEGMENTATION = [
    "amd/HRNet",
    "amd/SemanticFPN",
]

RYZEN_PREQUANTIZED_MODEL_IMAGE_TO_IMAGE = ["amd/PAN", "amd/rcan", "amd/sesr"]

RYZEN_PREQUANTIZED_MODEL_CUSTOM_TASKS = ["amd/movenet"]

PYTORCH_TIMM_MODEL_SUBSET = {
    "default-timm-config": {
        "timm/densenet121.ra_in1k": ["image-classification"],
        "timm/ese_vovnet19b_dw.ra_in1k": ["image-classification"],
        "timm/ghostnet_100.in1k": ["image-classification"],
        "timm/inception_v4.tf_in1k": ["image-classification"],
        "timm/repvgg_b0.rvgg_in1k": ["image-classification"],
        "timm/resnet10t.c3_in1k": ["image-classification"],
        "timm/vgg19.tv_in1k": ["image-classification"],
    }
}

PYTORCH_TIMM_MODEL = {
    "default-timm-config": {
        "timm/botnet26t_256.c1_in1k": ["image-classification"],
        "timm/cs3darknet_focus_l.c2ns_in1k": ["image-classification"],
        "timm/cs3darknet_focus_m.c2ns_in1k": ["image-classification"],
        "timm/cs3darknet_l.c2ns_in1k": ["image-classification"],
        "timm/cs3darknet_m.c2ns_in1k": ["image-classification"],
        "timm/cs3darknet_x.c2ns_in1k": ["image-classification"],
        "timm/cs3edgenet_x.c2_in1k": ["image-classification"],
        "timm/cs3se_edgenet_x.c2ns_in1k": ["image-classification"],
        "timm/cs3sedarknet_l.c2ns_in1k": ["image-classification"],
        "timm/cs3sedarknet_x.c2ns_in1k": ["image-classification"],
        "timm/cspdarknet53.ra_in1k": ["image-classification"],
        "timm/cspresnet50.ra_in1k": ["image-classification"],
        "timm/cspresnext50.ra_in1k": ["image-classification"],
        "timm/densenet121.ra_in1k": ["image-classification"],
        "timm/densenet169.tv_in1k": ["image-classification"],
        "timm/densenetblur121d.ra_in1k": ["image-classification"],
        "timm/dla102.in1k": ["image-classification"],
        "timm/dla102x.in1k": ["image-classification"],
        "timm/dla102x2.in1k": ["image-classification"],
        "timm/dla169.in1k": ["image-classification"],
        "timm/dla34.in1k": ["image-classification"],
        "timm/dla46_c.in1k": ["image-classification"],
        "timm/dla46x_c.in1k": ["image-classification"],
        "timm/dla60.in1k": ["image-classification"],
        "timm/dla60_res2net.in1k": ["image-classification"],
        "timm/dla60_res2next.in1k": ["image-classification"],
        "timm/dla60x.in1k": ["image-classification"],
        "timm/dla60x_c.in1k": ["image-classification"],
        "timm/dpn68.mx_in1k": ["image-classification"],
        "timm/dpn68b.ra_in1k": ["image-classification"],
        "timm/dpn92.mx_in1k": ["image-classification"],
        "timm/dpn98.mx_in1k": ["image-classification"],
        "timm/eca_botnext26ts_256.c1_in1k": ["image-classification"],
        "timm/eca_nfnet_l0.ra2_in1k": ["image-classification"],
        "timm/eca_resnet33ts.ra2_in1k": ["image-classification"],
        "timm/eca_resnext26ts.ch_in1k": ["image-classification"],
        "timm/ecaresnet101d.miil_in1k": ["image-classification"],
        "timm/ecaresnet101d_pruned.miil_in1k": ["image-classification"],
        "timm/ecaresnet26t.ra2_in1k": ["image-classification"],
        "timm/ecaresnet50d.miil_in1k": ["image-classification"],
        "timm/ecaresnet50d_pruned.miil_in1k": ["image-classification"],
        "timm/ecaresnet50t.ra2_in1k": ["image-classification"],
        "timm/ecaresnetlight.miil_in1k": ["image-classification"],
        "timm/edgenext_base.usi_in1k": ["image-classification"],
        "timm/edgenext_small.usi_in1k": ["image-classification"],
        "timm/edgenext_small_rw.sw_in1k": ["image-classification"],
        "timm/edgenext_x_small.in1k": ["image-classification"],
        "timm/edgenext_xx_small.in1k": ["image-classification"],
        "timm/efficientnet_b0.ra_in1k": ["image-classification"],
        "timm/efficientnet_b1.ft_in1k": ["image-classification"],
        "timm/efficientnet_b2.ra_in1k": ["image-classification"],
        "timm/efficientnet_b3.ra2_in1k": ["image-classification"],
        "timm/efficientnet_el.ra_in1k": ["image-classification"],
        "timm/efficientnet_el_pruned.in1k": ["image-classification"],
        "timm/efficientnet_em.ra2_in1k": ["image-classification"],
        "timm/efficientnet_es.ra_in1k": ["image-classification"],
        "timm/efficientnet_es_pruned.in1k": ["image-classification"],
        "timm/efficientnet_lite0.ra_in1k": ["image-classification"],
        "timm/efficientnetv2_rw_s.ra2_in1k": ["image-classification"],
        "timm/efficientnetv2_rw_t.ra2_in1k": ["image-classification"],
        "timm/ese_vovnet19b_dw.ra_in1k": ["image-classification"],
        "timm/ese_vovnet39b.ra_in1k": ["image-classification"],
        "timm/fbnetc_100.rmsp_in1k": ["image-classification"],
        "timm/fbnetv3_b.ra2_in1k": ["image-classification"],
        "timm/fbnetv3_d.ra2_in1k": ["image-classification"],
        "timm/fbnetv3_g.ra2_in1k": ["image-classification"],
        "timm/gcresnet33ts.ra2_in1k": ["image-classification"],
        "timm/gcresnet50t.ra2_in1k": ["image-classification"],
        "timm/gcresnext26ts.ch_in1k": ["image-classification"],
        "timm/gcresnext50ts.ch_in1k": ["image-classification"],
        "timm/gernet_l.idstcv_in1k": ["image-classification"],
        "timm/gernet_m.idstcv_in1k": ["image-classification"],
        "timm/gernet_s.idstcv_in1k": ["image-classification"],
        "timm/ghostnet_100.in1k": ["image-classification"],
        "timm/hardcorenas_a.miil_green_in1k": ["image-classification"],
        "timm/hardcorenas_b.miil_green_in1k": ["image-classification"],
        "timm/hardcorenas_c.miil_green_in1k": ["image-classification"],
        "timm/hardcorenas_d.miil_green_in1k": ["image-classification"],
        "timm/hardcorenas_e.miil_green_in1k": ["image-classification"],
        "timm/hardcorenas_f.miil_green_in1k": ["image-classification"],
        "timm/hrnet_w18_small.gluon_in1k": ["image-classification"],
        "timm/hrnet_w18_small_v2.gluon_in1k": ["image-classification"],
        "timm/inception_v3.gluon_in1k": ["image-classification"],
        "timm/inception_v3.tf_adv_in1k": ["image-classification"],
        "timm/inception_v3.tf_in1k": ["image-classification"],
        "timm/inception_v3.tv_in1k": ["image-classification"],
        "timm/inception_v4.tf_in1k": ["image-classification"],
        "timm/lambda_resnet26rpt_256.c1_in1k": ["image-classification"],
        "timm/lambda_resnet26t.c1_in1k": ["image-classification"],
        "timm/lambda_resnet50ts.a1h_in1k": ["image-classification"],
        "timm/lcnet_050.ra2_in1k": ["image-classification"],
        "timm/lcnet_075.ra2_in1k": ["image-classification"],
        "timm/lcnet_100.ra2_in1k": ["image-classification"],
        "timm/mixer_b16_224.goog_in21k_ft_in1k": ["image-classification"],
        "timm/mixer_b16_224.miil_in21k_ft_in1k": ["image-classification"],
        "timm/mixnet_l.ft_in1k": ["image-classification"],
        "timm/mixnet_m.ft_in1k": ["image-classification"],
        "timm/mixnet_s.ft_in1k": ["image-classification"],
        "timm/mnasnet_100.rmsp_in1k": ["image-classification"],
        "timm/mnasnet_small.lamb_in1k": ["image-classification"],
        "timm/mobilenetv2_050.lamb_in1k": ["image-classification"],
        "timm/mobilenetv2_100.ra_in1k": ["image-classification"],
        "timm/mobilenetv2_110d.ra_in1k": ["image-classification"],
        "timm/mobilenetv2_120d.ra_in1k": ["image-classification"],
        "timm/mobilenetv2_140.ra_in1k": ["image-classification"],
        "timm/mobilenetv3_large_100.miil_in21k_ft_in1k": ["image-classification"],
        "timm/mobilenetv3_large_100.ra_in1k": ["image-classification"],
        "timm/mobilenetv3_rw.rmsp_in1k": ["image-classification"],
        "timm/mobilenetv3_small_050.lamb_in1k": ["image-classification"],
        "timm/mobilenetv3_small_075.lamb_in1k": ["image-classification"],
        "timm/mobilenetv3_small_100.lamb_in1k": ["image-classification"],
        "timm/nest_tiny_jx.goog_in1k": ["image-classification"],
        "timm/nf_resnet50.ra2_in1k": ["image-classification"],
        "timm/nfnet_l0.ra2_in1k": ["image-classification"],
        "timm/regnetx_002.pycls_in1k": ["image-classification"],
        "timm/regnetx_004.pycls_in1k": ["image-classification"],
        "timm/regnetx_004_tv.tv2_in1k": ["image-classification"],
        "timm/regnetx_006.pycls_in1k": ["image-classification"],
        "timm/regnetx_008.pycls_in1k": ["image-classification"],
        "timm/regnetx_008.tv2_in1k": ["image-classification"],
        "timm/regnetx_016.pycls_in1k": ["image-classification"],
        "timm/regnetx_016.tv2_in1k": ["image-classification"],
        "timm/regnetx_032.pycls_in1k": ["image-classification"],
        "timm/regnetx_032.tv2_in1k": ["image-classification"],
        "timm/regnetx_040.pycls_in1k": ["image-classification"],
        "timm/regnetx_064.pycls_in1k": ["image-classification"],
        "timm/regnetx_080.pycls_in1k": ["image-classification"],
        "timm/regnetx_080.tv2_in1k": ["image-classification"],
        "timm/regnetx_120.pycls_in1k": ["image-classification"],
        "timm/regnetx_160.pycls_in1k": ["image-classification"],
        "timm/regnetx_160.tv2_in1k": ["image-classification"],
        "timm/regnety_002.pycls_in1k": ["image-classification"],
        "timm/regnety_004.pycls_in1k": ["image-classification"],
        "timm/regnety_004.tv2_in1k": ["image-classification"],
        "timm/regnety_006.pycls_in1k": ["image-classification"],
        "timm/regnety_008.pycls_in1k": ["image-classification"],
        "timm/regnety_008_tv.tv2_in1k": ["image-classification"],
        "timm/regnety_016.pycls_in1k": ["image-classification"],
        "timm/regnety_016.tv2_in1k": ["image-classification"],
        "timm/regnety_032.pycls_in1k": ["image-classification"],
        "timm/regnety_032.ra_in1k": ["image-classification"],
        "timm/regnety_032.tv2_in1k": ["image-classification"],
        "timm/regnety_040.pycls_in1k": ["image-classification"],
        "timm/regnety_040.ra3_in1k": ["image-classification"],
        "timm/regnety_064.pycls_in1k": ["image-classification"],
        "timm/regnety_064.ra3_in1k": ["image-classification"],
        "timm/regnety_080.pycls_in1k": ["image-classification"],
        "timm/regnety_080.ra3_in1k": ["image-classification"],
        "timm/regnety_080_tv.tv2_in1k": ["image-classification"],
        "timm/regnety_120.pycls_in1k": ["image-classification"],
        "timm/regnety_120.sw_in12k_ft_in1k": ["image-classification"],
        "timm/regnety_160.lion_in12k_ft_in1k": ["image-classification"],
        "timm/regnety_160.pycls_in1k": ["image-classification"],
        "timm/regnety_160.sw_in12k_ft_in1k": ["image-classification"],
        "timm/regnety_160.swag_ft_in1k": ["image-classification"],
        "timm/regnety_160.swag_lc_in1k": ["image-classification"],
        "timm/regnety_160.tv2_in1k": ["image-classification"],
        "timm/regnety_320.seer_ft_in1k": ["image-classification"],
        "timm/regnety_320.swag_ft_in1k": ["image-classification"],
        "timm/regnetz_040.ra3_in1k": ["image-classification"],
        "timm/regnetz_040_h.ra3_in1k": ["image-classification"],
        "timm/regnetz_b16.ra3_in1k": ["image-classification"],
        "timm/regnetz_c16.ra3_in1k": ["image-classification"],
        "timm/regnetz_d32.ra3_in1k": ["image-classification"],
        "timm/regnetz_d8.ra3_in1k": ["image-classification"],
        "timm/repvgg_a2.rvgg_in1k": ["image-classification"],
        "timm/repvgg_b0.rvgg_in1k": ["image-classification"],
        "timm/repvgg_b1.rvgg_in1k": ["image-classification"],
        "timm/repvgg_b1g4.rvgg_in1k": ["image-classification"],
        "timm/repvgg_b2.rvgg_in1k": ["image-classification"],
        "timm/repvgg_b2g4.rvgg_in1k": ["image-classification"],
        "timm/repvgg_b3.rvgg_in1k": ["image-classification"],
        "timm/repvgg_b3g4.rvgg_in1k": ["image-classification"],
        "timm/res2net50_14w_8s.in1k": ["image-classification"],
        "timm/res2net50_26w_4s.in1k": ["image-classification"],
        "timm/res2net50_26w_6s.in1k": ["image-classification"],
        "timm/res2net50_26w_8s.in1k": ["image-classification"],
        "timm/res2net50_48w_2s.in1k": ["image-classification"],
        "timm/res2next50.in1k": ["image-classification"],
        "timm/resmlp_12_224.fb_distilled_in1k": ["image-classification"],
        "timm/resmlp_12_224.fb_in1k": ["image-classification"],
        "timm/resmlp_24_224.fb_distilled_in1k": ["image-classification"],
        "timm/resmlp_24_224.fb_in1k": ["image-classification"],
        "timm/resmlp_big_24_224.fb_distilled_in1k": ["image-classification"],
        "timm/resnest14d.gluon_in1k": ["image-classification"],
        "timm/resnest26d.gluon_in1k": ["image-classification"],
        "timm/resnest50d.in1k": ["image-classification"],
        "timm/resnest50d_1s4x24d.in1k": ["image-classification"],
        "timm/resnest50d_4s2x40d.in1k": ["image-classification"],
        "timm/resnet101.a1h_in1k": ["image-classification"],
        "timm/resnet101.gluon_in1k": ["image-classification"],
        "timm/resnet101.tv_in1k": ["image-classification"],
        "timm/resnet101c.gluon_in1k": ["image-classification"],
        "timm/resnet101d.gluon_in1k": ["image-classification"],
        "timm/resnet101d.ra2_in1k": ["image-classification"],
        "timm/resnet101s.gluon_in1k": ["image-classification"],
        "timm/resnet10t.c3_in1k": ["image-classification"],
        "timm/resnet14t.c3_in1k": ["image-classification"],
        "timm/resnet152.a1h_in1k": ["image-classification"],
        "timm/resnet152.gluon_in1k": ["image-classification"],
        "timm/resnet152.tv_in1k": ["image-classification"],
        "timm/resnet152c.gluon_in1k": ["image-classification"],
        "timm/resnet152d.gluon_in1k": ["image-classification"],
        "timm/resnet152d.ra2_in1k": ["image-classification"],
        "timm/resnet152s.gluon_in1k": ["image-classification"],
        "timm/resnet18.a1_in1k": ["image-classification"],
        "timm/resnet18.fb_ssl_yfcc100m_ft_in1k": ["image-classification"],
        "timm/resnet18.fb_swsl_ig1b_ft_in1k": ["image-classification"],
        "timm/resnet18.gluon_in1k": ["image-classification"],
        "timm/resnet18d.ra2_in1k": ["image-classification"],
        "timm/resnet200d.ra2_in1k": ["image-classification"],
        "timm/resnet26.bt_in1k": ["image-classification"],
        "timm/resnet26d.bt_in1k": ["image-classification"],
        "timm/resnet26t.ra2_in1k": ["image-classification"],
        "timm/resnet32ts.ra2_in1k": ["image-classification"],
        "timm/resnet33ts.ra2_in1k": ["image-classification"],
        "timm/resnet34.a1_in1k": ["image-classification"],
        "timm/resnet34.gluon_in1k": ["image-classification"],
        "timm/resnet34.tv_in1k": ["image-classification"],
        "timm/resnet34d.ra2_in1k": ["image-classification"],
        "timm/resnet50.a1_in1k": ["image-classification"],
        "timm/resnet50.fb_ssl_yfcc100m_ft_in1k": ["image-classification"],
        "timm/resnet50.fb_swsl_ig1b_ft_in1k": ["image-classification"],
        "timm/resnet50.gluon_in1k": ["image-classification"],
        "timm/resnet50.tv_in1k": ["image-classification"],
        "timm/resnet50_gn.a1h_in1k": ["image-classification"],
        "timm/resnet50c.gluon_in1k": ["image-classification"],
        "timm/resnet50d.gluon_in1k": ["image-classification"],
        "timm/resnet50d.ra2_in1k": ["image-classification"],
        "timm/resnet50s.gluon_in1k": ["image-classification"],
        "timm/resnet51q.ra2_in1k": ["image-classification"],
        "timm/resnet61q.ra2_in1k": ["image-classification"],
        "timm/resnetaa50.a1h_in1k": ["image-classification"],
        "timm/resnetblur50.bt_in1k": ["image-classification"],
        "timm/resnetrs101.tf_in1k": ["image-classification"],
        "timm/resnetrs50.tf_in1k": ["image-classification"],
        "timm/resnetv2_101.a1h_in1k": ["image-classification"],
        "timm/resnetv2_50.a1h_in1k": ["image-classification"],
        "timm/resnetv2_50d_gn.ah_in1k": ["image-classification"],
        "timm/resnetv2_50x1_bit.goog_distilled_in1k": ["image-classification"],
        "timm/resnetv2_50x1_bit.goog_in21k_ft_in1k": ["image-classification"],
        "timm/resnetv2_50x3_bit.goog_in21k_ft_in1k": ["image-classification"],
        "timm/resnext101_32x4d.fb_ssl_yfcc100m_ft_in1k": ["image-classification"],
        "timm/resnext101_32x4d.fb_swsl_ig1b_ft_in1k": ["image-classification"],
        "timm/resnext101_32x4d.gluon_in1k": ["image-classification"],
        "timm/resnext101_32x8d.fb_ssl_yfcc100m_ft_in1k": ["image-classification"],
        "timm/resnext101_32x8d.fb_swsl_ig1b_ft_in1k": ["image-classification"],
        "timm/resnext101_32x8d.fb_wsl_ig1b_ft_in1k": ["image-classification"],
        "timm/resnext101_64x4d.c1_in1k": ["image-classification"],
        "timm/resnext101_64x4d.gluon_in1k": ["image-classification"],
        "timm/resnext26ts.ra2_in1k": ["image-classification"],
        "timm/resnext50_32x4d.a1h_in1k": ["image-classification"],
        "timm/resnext50_32x4d.fb_ssl_yfcc100m_ft_in1k": ["image-classification"],
        "timm/resnext50_32x4d.fb_swsl_ig1b_ft_in1k": ["image-classification"],
        "timm/resnext50_32x4d.gluon_in1k": ["image-classification"],
        "timm/resnext50_32x4d.tv_in1k": ["image-classification"],
        "timm/resnext50d_32x4d.bt_in1k": ["image-classification"],
        "timm/rexnet_100.nav_in1k": ["image-classification"],
        "timm/rexnet_130.nav_in1k": ["image-classification"],
        "timm/rexnet_150.nav_in1k": ["image-classification"],
        "timm/rexnet_200.nav_in1k": ["image-classification"],
        "timm/rexnet_300.nav_in1k": ["image-classification"],
        "timm/rexnetr_200.sw_in12k_ft_in1k": ["image-classification"],
        "timm/rexnetr_300.sw_in12k_ft_in1k": ["image-classification"],
        "timm/sebotnet33ts_256.a1h_in1k": ["image-classification"],
        "timm/semnasnet_075.rmsp_in1k": ["image-classification"],
        "timm/semnasnet_100.rmsp_in1k": ["image-classification"],
        "timm/seresnet33ts.ra2_in1k": ["image-classification"],
        "timm/seresnet50.a1_in1k": ["image-classification"],
        "timm/seresnext101_32x4d.gluon_in1k": ["image-classification"],
        "timm/seresnext26d_32x4d.bt_in1k": ["image-classification"],
        "timm/seresnext26t_32x4d.bt_in1k": ["image-classification"],
        "timm/seresnext26ts.ch_in1k": ["image-classification"],
        "timm/seresnext50_32x4d.gluon_in1k": ["image-classification"],
        "timm/seresnext50_32x4d.racm_in1k": ["image-classification"],
        "timm/skresnet18.ra_in1k": ["image-classification"],
        "timm/skresnet34.ra_in1k": ["image-classification"],
        "timm/skresnext50_32x4d.ra_in1k": ["image-classification"],
        "timm/spnasnet_100.rmsp_in1k": ["image-classification"],
        "timm/tf_efficientnet_el.in1k": ["image-classification"],
        "timm/tf_efficientnet_em.in1k": ["image-classification"],
        "timm/tf_efficientnet_es.in1k": ["image-classification"],
        "timm/tf_efficientnet_lite0.in1k": ["image-classification"],
        "timm/tf_efficientnet_lite1.in1k": ["image-classification"],
        "timm/tf_efficientnet_lite2.in1k": ["image-classification"],
        "timm/tf_efficientnet_lite3.in1k": ["image-classification"],
        "timm/tf_efficientnet_lite4.in1k": ["image-classification"],
        "timm/tf_efficientnetv2_b0.in1k": ["image-classification"],
        "timm/tf_efficientnetv2_b1.in1k": ["image-classification"],
        "timm/tf_efficientnetv2_b2.in1k": ["image-classification"],
        "timm/tf_efficientnetv2_b3.in1k": ["image-classification"],
        "timm/tf_efficientnetv2_b3.in21k_ft_in1k": ["image-classification"],
        "timm/tf_mobilenetv3_large_minimal_100.in1k": ["image-classification"],
        "timm/tf_mobilenetv3_small_075.in1k": ["image-classification"],
        "timm/tf_mobilenetv3_small_100.in1k": ["image-classification"],
        "timm/tf_mobilenetv3_small_minimal_100.in1k": ["image-classification"],
        "timm/tinynet_a.in1k": ["image-classification"],
        "timm/tinynet_d.in1k": ["image-classification"],
        "timm/vgg11.tv_in1k": ["image-classification"],
        "timm/vgg11_bn.tv_in1k": ["image-classification"],
        "timm/vgg13.tv_in1k": ["image-classification"],
        "timm/vgg13_bn.tv_in1k": ["image-classification"],
        "timm/vgg16.tv_in1k": ["image-classification"],
        "timm/vgg16_bn.tv_in1k": ["image-classification"],
        "timm/vgg19.tv_in1k": ["image-classification"],
        "timm/vgg19_bn.tv_in1k": ["image-classification"],
        "timm/wide_resnet101_2.tv_in1k": ["image-classification"],
        "timm/wide_resnet50_2.racm_in1k": ["image-classification"],
        "timm/xception41.tf_in1k": ["image-classification"],
        "timm/xception41p.ra3_in1k": ["image-classification"],
        "timm/xception65.ra3_in1k": ["image-classification"],
        "timm/xception65p.ra3_in1k": ["image-classification"],
        "timm/xception71.tf_in1k": ["image-classification"],
    }
}
