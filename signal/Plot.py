import matplotlib
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from neurokit2 import ecg_segment, ppg_segment
from neurokit2.ecg.ecg_peaks import _ecg_peaks_plot
from neurokit2.eda.eda_plot import _eda_plot_dashedsegments
from neurokit2.emg.emg_plot import _emg_plot_activity
from neurokit2.ppg.ppg_peaks import _ppg_peaks_plot
from neurokit2.rsp.rsp_plot import _rsp_plot_phase
from neurokit2.signal.signal_rate import _signal_rate_plot


def ecg_pre_plot(id,ecg_signals,info=None):
    fig, ax0 = plt.subplots(figsize=(8,6))
    fig.suptitle("ECG--ID:" + id + "'s Preprocess Result", fontweight="bold")
    phase = None
    if "ECG_Phase_Ventricular" in ecg_signals.columns:
        phase = ecg_signals["ECG_Phase_Ventricular"].values
    ax0 = _ecg_peaks_plot(
        ecg_signals["ECG_Clean"].values,
        info=info,
        sampling_rate=info["sampling_rate"],
        raw=ecg_signals["ECG_Raw"].values,
        quality=ecg_signals["ECG_Quality"].values,
        phase=phase,
        ax=ax0,
    )

def ecg_res_plot(id, ecg_signals, info=None):
    # Extract R-peaks (take those from df as it might have been cropped)
    # Prepare figure and set axes.
    gs = matplotlib.gridspec.GridSpec(2, 2, width_ratios=[2 / 3, 1 / 3])
    fig = plt.figure(constrained_layout=False, figsize=(12, 8.73))
    fig.suptitle("ECG--ID:" + id + "'s QuickProcess Result", fontweight="bold")
    ax0 = fig.add_subplot(gs[0, :-1])
    ax1 = fig.add_subplot(gs[1, :-1], sharex=ax0)
    ax2 = fig.add_subplot(gs[:, -1])
    # Plot signals
    phase = None
    if "ECG_Phase_Ventricular" in ecg_signals.columns:
        phase = ecg_signals["ECG_Phase_Ventricular"].values
    ax0 = _ecg_peaks_plot(
        ecg_signals["ECG_Clean"].values,
        info=info,
        sampling_rate=info["sampling_rate"],
        raw=ecg_signals["ECG_Raw"].values,
        quality=ecg_signals["ECG_Quality"].values,
        phase=phase,
        ax=ax0,
    )

    # Plot Heart Rate
    ax1 = _signal_rate_plot(
        ecg_signals["ECG_Rate"].values,
        info["ECG_R_Peaks"],
        sampling_rate=info["sampling_rate"],
        title="Heart Rate",
        ytitle="Beats per minute (bpm)",
        color="#FF5722",
        color_mean="#FF9800",
        color_points="#FFC107",
        ax=ax1,
    )

    # Plot individual heart beats
    ax2 = ecg_segment(
        ecg_signals,
        info["ECG_R_Peaks"],
        info["sampling_rate"],
        show="return",
        ax=ax2,
    )


def ecg_extract_res_plot(id, ecg_signals, info):
    gs = matplotlib.gridspec.GridSpec(2, 1)
    fig = plt.figure(constrained_layout=False, figsize=(12, 8.73))
    fig.suptitle("ECG--ID:" + id + "'s Extract Result", fontweight="bold")
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])

    # Plot signals
    phase = None
    if "ECG_Phase_Ventricular" in ecg_signals.columns:
        phase = ecg_signals["ECG_Phase_Ventricular"].values
    # Plot Heart Rate
    ax1 = _signal_rate_plot(
        ecg_signals["ECG_Rate"].values,
        info["ECG_R_Peaks"],
        sampling_rate=info["sampling_rate"],
        title="Heart Rate",
        ytitle="Beats per minute (bpm)",
        color="#FF5722",
        color_mean="#FF9800",
        color_points="#FFC107",
        ax=ax1,
    )

    # Plot individual heart beats
    ax2 = ecg_segment(
        ecg_signals,
        info["ECG_R_Peaks"],
        info["sampling_rate"],
        show="return",
        ax=ax2,
    )
    plt.show()


def ppg_extract_res_plot(id, ppg_signals, info):
    gs = matplotlib.gridspec.GridSpec(2, 1)
    fig = plt.figure(constrained_layout=False, figsize=(12, 8.73))
    fig.suptitle("PPG--ID:" + id + "'s Extract Result", fontweight="bold")
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    # Plot Heart Rate
    ax1 = _signal_rate_plot(
        ppg_signals["PPG_Rate"].values,
        info["PPG_Peaks"],
        sampling_rate=info["sampling_rate"],
        title="Heart Rate",
        ytitle="Beats per minute (bpm)",
        color="#FB661C",
        color_mean="#FBB41C",
        color_points="#FF9800",
        ax=ax1,
    )
    # Plot individual heart beats
    ax2 = ppg_segment(
        ppg_signals["PPG_Clean"].values,
        info["PPG_Peaks"],
        info["sampling_rate"],
        show="return",
        ax=ax2, )



def ppg_res_plot(id, ppg_signals, info=None):
    # Extract R-peaks (take those from df as it might have been cropped)
    # Prepare figure and set axes.
    gs = matplotlib.gridspec.GridSpec(2, 2, width_ratios=[2 / 3, 1 / 3])

    fig = plt.figure(constrained_layout=False, figsize=(12, 8.73))
    fig.suptitle("PPG--ID:" + id + "'s QuickProcess Result", fontweight="bold")

    ax0 = fig.add_subplot(gs[0, :-1])
    ax1 = fig.add_subplot(gs[1, :-1], sharex=ax0)
    ax2 = fig.add_subplot(gs[:, -1])

    ax0 = _ppg_peaks_plot(
        ppg_signals["PPG_Clean"].values,
        info=info,
        sampling_rate=info["sampling_rate"],
        raw=ppg_signals["PPG_Raw"].values,
        ax=ax0,
    )

    # Plot Heart Rate
    ax1 = _signal_rate_plot(
        ppg_signals["PPG_Rate"].values,
        info["PPG_Peaks"],
        sampling_rate=info["sampling_rate"],
        title="Heart Rate",
        ytitle="Beats per minute (bpm)",
        color="#FB661C",
        color_mean="#FBB41C",
        color_points="#FF9800",
        ax=ax1,
    )

    # Plot individual heart beats
    ax2 = ppg_segment(
        ppg_signals["PPG_Clean"].values,
        info["PPG_Peaks"],
        info["sampling_rate"],
        show="return",
        ax=ax2, )


def rsp_res_plot(id,type, rsp_signals, info=None, static=True):
    # Mark peaks, troughs and phases.
    peaks = np.where(rsp_signals["RSP_Peaks"] == 1)[0]
    troughs = np.where(rsp_signals["RSP_Troughs"] == 1)[0]
    inhale = np.where(rsp_signals["RSP_Phase"] == 1)[0]
    exhale = np.where(rsp_signals["RSP_Phase"] == 0)[0]

    nrow = 2

    # Determine mean rate.
    rate_mean = np.mean(rsp_signals["RSP_Rate"])

    if "RSP_Amplitude" in list(rsp_signals.columns):
        nrow += 1
        # Determine mean amplitude.
        amplitude_mean = np.mean(rsp_signals["RSP_Amplitude"])
    if "RSP_RVT" in list(rsp_signals.columns):
        nrow += 1
        # Determine mean RVT.
        rvt_mean = np.mean(rsp_signals["RSP_RVT"])
    if "RSP_Symmetry_PeakTrough" in list(rsp_signals.columns):
        nrow += 1

    # Get signals marking inspiration and expiration.
    exhale_signal, inhale_signal = _rsp_plot_phase(rsp_signals, troughs, peaks)

    # Determine unit of x-axis.
    x_label = "Time (seconds)"
    x_axis = np.linspace(0, len(rsp_signals) / info["sampling_rate"], len(rsp_signals))

    if static:
        fig, ax = plt.subplots(nrows=nrow, ncols=1, sharex=True, figsize=(12, 8.73))
        last_ax = fig.get_axes()[-1]
        last_ax.set_xlabel(x_label)
        # Plot cleaned and raw respiration as well as peaks and troughs.
        ax[0].set_title("Raw and Cleaned Signal")
        if type:
            fig.suptitle("Respiration(RSP)" + "--ID:" + id+"'s QuickProcess Result", fontweight="bold")
        else:
            fig.suptitle("Respiration(RSP)" + "--ID:" + id + "'s Extract Result", fontweight="bold")
        ax[0].plot(
            x_axis, rsp_signals["RSP_Raw"], color="#B0BEC5", label="Raw", zorder=1
        )
        ax[0].plot(
            x_axis,
            rsp_signals["RSP_Clean"],
            color="#2196F3",
            label="Cleaned",
            zorder=2,
            linewidth=1.5,
        )
        ax[0].scatter(
            x_axis[peaks],
            rsp_signals["RSP_Clean"][peaks],
            color="red",
            label="Exhalation Onsets",
            zorder=3,
        )
        ax[0].scatter(
            x_axis[troughs],
            rsp_signals["RSP_Clean"][troughs],
            color="orange",
            label="Inhalation Onsets",
            zorder=4,
        )

        # Shade region to mark inspiration and expiration.
        ax[0].fill_between(
            x_axis[exhale],
            exhale_signal[exhale],
            rsp_signals["RSP_Clean"][exhale],
            where=rsp_signals["RSP_Clean"][exhale] > exhale_signal[exhale],
            color="#CFD8DC",
            linestyle="None",
            label="exhalation",
        )
        ax[0].fill_between(
            x_axis[inhale],
            inhale_signal[inhale],
            rsp_signals["RSP_Clean"][inhale],
            where=rsp_signals["RSP_Clean"][inhale] > inhale_signal[inhale],
            color="#ECEFF1",
            linestyle="None",
            label="inhalation",
        )

        ax[0].legend(loc="upper right")

        # Plot rate and optionally amplitude.
        ax[1].set_title("Breathing Rate")
        ax[1].plot(
            x_axis,
            rsp_signals["RSP_Rate"],
            color="#4CAF50",
            label="Rate",
            linewidth=1.5,
        )
        ax[1].axhline(y=rate_mean, label="Mean", linestyle="--", color="#4CAF50")
        ax[1].legend(loc="upper right")

        if "RSP_Amplitude" in list(rsp_signals.columns):
            ax[2].set_title("Breathing Amplitude")

            ax[2].plot(
                x_axis,
                rsp_signals["RSP_Amplitude"],
                color="#009688",
                label="Amplitude",
                linewidth=1.5,
            )
            ax[2].axhline(
                y=amplitude_mean, label="Mean", linestyle="--", color="#009688"
            )
            ax[2].legend(loc="upper right")

        if "RSP_RVT" in list(rsp_signals.columns):
            ax[3].set_title("Respiratory Volume per Time")

            ax[3].plot(
                x_axis,
                rsp_signals["RSP_RVT"],
                color="#00BCD4",
                label="RVT",
                linewidth=1.5,
            )
            ax[3].axhline(y=rvt_mean, label="Mean", linestyle="--", color="#009688")
            ax[3].legend(loc="upper right")

        if "RSP_Symmetry_PeakTrough" in list(rsp_signals.columns):
            ax[4].set_title("Cycle Symmetry")

            ax[4].plot(
                x_axis,
                rsp_signals["RSP_Symmetry_PeakTrough"],
                color="green",
                label="Peak-Trough Symmetry",
                linewidth=1.5,
            )
            ax[4].plot(
                x_axis,
                rsp_signals["RSP_Symmetry_RiseDecay"],
                color="purple",
                label="Rise-Decay Symmetry",
                linewidth=1.5,
            )
            ax[4].legend(loc="upper right")
    else:
        # Generate interactive plot with plotly.
        try:
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots

        except ImportError as e:
            raise ImportError(
                "NeuroKit error: rsp_plot(): the 'plotly'",
                " module is required when 'static' is False.",
                " Please install it first (`pip install plotly`).",
            ) from e

        subplot_titles = ["Raw and Cleaned Signal", "Breathing Rate"]
        if "RSP_Amplitude" in list(rsp_signals.columns):
            subplot_titles.append("Breathing Amplitude")
        if "RSP_RVT" in list(rsp_signals.columns):
            subplot_titles.append("Respiratory Volume per Time")
        if "RSP_Symmetry_PeakTrough" in list(rsp_signals.columns):
            subplot_titles.append("Cycle Symmetry")
        subplot_titles = tuple(subplot_titles)
        fig = make_subplots(
            rows=nrow,
            cols=1,
            shared_xaxes=True,
            subplot_titles=subplot_titles,
        )

        # Plot cleaned and raw RSP
        fig.add_trace(
            go.Scatter(
                x=x_axis, y=rsp_signals["RSP_Raw"], name="Raw", marker_color="#B0BEC5"
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=x_axis,
                y=rsp_signals["RSP_Clean"],
                name="Cleaned",
                marker_color="#2196F3",
            ),
            row=1,
            col=1,
        )

        # Plot peaks and troughs.
        fig.add_trace(
            go.Scatter(
                x=x_axis[peaks],
                y=rsp_signals["RSP_Clean"][peaks],
                name="Exhalation Onsets",
                marker_color="red",
                mode="markers",
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=x_axis[troughs],
                y=rsp_signals["RSP_Clean"][troughs],
                name="Inhalation Onsets",
                marker_color="orange",
                mode="markers",
            ),
            row=1,
            col=1,
        )



        # Plot rate and optionally amplitude.
        fig.add_trace(
            go.Scatter(
                x=x_axis, y=rsp_signals["RSP_Rate"], name="Rate", marker_color="#4CAF50"
            ),
            row=2,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=x_axis,
                y=[rate_mean] * len(x_axis),
                name="Mean Rate",
                marker_color="#4CAF50",
                line=dict(dash="dash"),
            ),
            row=2,
            col=1,
        )

        if "RSP_Amplitude" in list(rsp_signals.columns):
            fig.add_trace(
                go.Scatter(
                    x=x_axis,
                    y=rsp_signals["RSP_Amplitude"],
                    name="Amplitude",
                    marker_color="#009688",
                ),
                row=3,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=x_axis,
                    y=[amplitude_mean] * len(x_axis),
                    name="Mean Amplitude",
                    marker_color="#009688",
                    line=dict(dash="dash"),
                ),
                row=3,
                col=1,
            )

        if "RSP_RVT" in list(rsp_signals.columns):
            fig.add_trace(
                go.Scatter(
                    x=x_axis,
                    y=rsp_signals["RSP_RVT"],
                    name="RVT",
                    marker_color="#00BCD4",
                ),
                row=4,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=x_axis,
                    y=[rvt_mean] * len(x_axis),
                    name="Mean RVT",
                    marker_color="#00BCD4",
                    line=dict(dash="dash"),
                ),
                row=4,
                col=1,
            )

        if "RSP_Symmetry_PeakTrough" in list(rsp_signals.columns):
            fig.add_trace(
                go.Scatter(
                    x=x_axis,
                    y=rsp_signals["RSP_Symmetry_PeakTrough"],
                    name="Peak-Trough Symmetry",
                    marker_color="green",
                ),
                row=5,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=x_axis,
                    y=rsp_signals["RSP_Symmetry_RiseDecay"],
                    name="Rise-Decay Symmetry",
                    marker_color="purple",
                ),
                row=5,
                col=1,
            )

        fig.update_layout(title_text="Respiration (RSP)", height=1250, width=750)
        for i in range(1, nrow + 1):
            fig.update_xaxes(title_text=x_label, row=i, col=1)
        return fig


def eda_preprocess_plot(id, eda_signals, sampling_rate, static=True):
    # Determine unit of x-axis.
    x_label = "Time (seconds)"
    x_axis = np.linspace(0, len(eda_signals) / sampling_rate, len(eda_signals))

    if static:
        fig, ax0 = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))

        # Plot cleaned and raw electrodermal activity.
        ax0.set_title("Raw and Cleaned Signal")
        fig.suptitle("EDA's Preprocess Result--ID:" + id, fontweight="bold")

        ax0.plot(x_axis, eda_signals["EDA_Raw"], color="#B0BEC5", label="Raw", zorder=1)
        ax0.plot(
            x_axis,
            eda_signals["EDA_Clean"],
            color="#9C27B0",
            label="Cleaned",
            linewidth=1.5,
            zorder=1,
        )
        ax0.legend(loc="upper right")
        # Set x label
        ax0.set_xlabel(x_label)

        # Adjust layout
        plt.tight_layout()


def eda_res_plot(id,type, eda_signals, info, static=True):
    # Determine peaks, onsets, and half recovery.
    peaks = np.where(eda_signals["SCR_Peaks"] == 1)[0]
    onsets = np.where(eda_signals["SCR_Onsets"] == 1)[0]
    half_recovery = np.where(eda_signals["SCR_Recovery"] == 1)[0]
    # clean peaks that do not have onsets
    if len(peaks) > len(onsets):
        peaks = peaks[1:]
    # Determine unit of x-axis.
    x_label = "Time (seconds)"
    x_axis = np.linspace(0, len(eda_signals) / info["sampling_rate"], len(eda_signals))
    if static:
        # type0表示绘制提取结果，type1表示绘制处理结果
        if type:
            fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(9, 6))
            fig.suptitle("EDA's QuickProcess Result--ID:" + id, fontweight="bold")
        else:
            fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(9, 6))
            fig.suptitle("EDA's Extract Result--ID:" + id, fontweight="bold")
        last_ax = fig.get_axes()[-1]
        last_ax.set_xlabel(x_label)
        if type:
            # Plot cleaned and raw electrodermal activity.
            ax0.set_title("Raw and Cleaned Signal")

            ax0.plot(x_axis, eda_signals["EDA_Raw"], color="#B0BEC5", label="Raw", zorder=1)
            ax0.plot(
                x_axis,
                eda_signals["EDA_Clean"],
                color="#9C27B0",
                label="Cleaned",
                linewidth=1.5,
                zorder=1,
            )
            ax0.legend(loc="upper right")

        # Plot skin conductance response.
        ax1.set_title("Skin Conductance Response (SCR)")

        # Plot Phasic.
        ax1.plot(
            x_axis,
            eda_signals["EDA_Phasic"],
            color="#E91E63",
            label="Phasic Component",
            linewidth=1.5,
            zorder=1,
        )

        # Mark segments.
        risetime_coord, amplitude_coord, halfr_coord = _eda_plot_dashedsegments(
            eda_signals, ax1, x_axis, onsets, peaks, half_recovery
        )

        risetime = matplotlib.collections.LineCollection(
            risetime_coord, colors="#FFA726", linewidths=1, linestyle="dashed"
        )
        ax1.add_collection(risetime)

        amplitude = matplotlib.collections.LineCollection(
            amplitude_coord, colors="#1976D2", linewidths=1, linestyle="solid"
        )
        ax1.add_collection(amplitude)

        halfr = matplotlib.collections.LineCollection(
            halfr_coord, colors="#FDD835", linewidths=1, linestyle="dashed"
        )
        ax1.add_collection(halfr)
        ax1.legend(loc="upper right")

        # Plot Tonic.
        ax2.set_title("Skin Conductance Level (SCL)")
        ax2.plot(
            x_axis,
            eda_signals["EDA_Tonic"],
            color="#673AB7",
            label="Tonic Component",
            linewidth=1.5,
        )
        ax2.legend(loc="upper right")


def emg_plot_static(id,type, emg_signals, x_axis, onsets, offsets, sampling_rate):
    # Prepare figure.
    if type:
        fig, (ax0, ax1) = plt.subplots(nrows=2, ncols=1, sharex=True,figsize=(8,8.4))
        fig.suptitle("EMG's QuickProcess Result--ID:" + id, fontweight="bold")
    else:
        fig, (ax1) = plt.subplots(nrows=1, ncols=1, sharex=True,figsize=(8,6))
        fig.suptitle("EMG's Extract Result--ID:" + id, fontweight="bold")
    if sampling_rate is not None:
        ax1.set_xlabel("Time (seconds)")
    elif sampling_rate is None:
        ax1.set_xlabel("Samples")
    plt.tight_layout(h_pad=0.2)
    if type:
        # Plot cleaned and raw EMG.
        ax0.set_title("Raw and Cleaned Signal")
        ax0.plot(x_axis, emg_signals["EMG_Raw"], color="#B0BEC5", label="Raw", zorder=1)
        ax0.plot(
            x_axis,
            emg_signals["EMG_Clean"],
            color="#FFC107",
            label="Cleaned",
            zorder=1,
            linewidth=1.5,
        )
        ax0.legend(loc="upper right")

    # Plot Amplitude.
    ax1.set_title("Muscle Activation")
    ax1.plot(
        x_axis,
        emg_signals["EMG_Amplitude"],
        color="#FF9800",
        label="Amplitude",
        linewidth=1.5,
    )

    # Shade activity regions.
    activity_signal = _emg_plot_activity(emg_signals, onsets, offsets)
    ax1.fill_between(
        x_axis,
        emg_signals["EMG_Amplitude"],
        activity_signal,
        where=emg_signals["EMG_Amplitude"] > activity_signal,
        color="#f7c568",
        alpha=0.5,
        label=None,
    )

    # Mark onsets and offsets.
    ax1.scatter(
        x_axis[onsets],
        emg_signals["EMG_Amplitude"][onsets],
        color="#f03e65",
        label=None,
        zorder=3,
    )
    ax1.scatter(
        x_axis[offsets],
        emg_signals["EMG_Amplitude"][offsets],
        color="#f03e65",
        label=None,
        zorder=3,
    )

    if sampling_rate is not None:
        onsets = onsets / sampling_rate
        offsets = offsets / sampling_rate

    for i, j in zip(list(onsets), list(offsets)):
        ax1.axvline(i, color="#4a4a4a", linestyle="--", label=None, zorder=2)
        ax1.axvline(j, color="#4a4a4a", linestyle="--", label=None, zorder=2)
    ax1.legend(loc="upper right")


def emg_res_plot(id,type, emg_signals, info):
    # Mark onsets, offsets, activity
    onsets = np.where(emg_signals["EMG_Onsets"] == 1)[0]
    offsets = np.where(emg_signals["EMG_Offsets"] == 1)[0]
    # Sanity-check input.
    if not isinstance(emg_signals, pd.DataFrame):
        raise ValueError(
            "NeuroKit error: The `emg_signals` argument must"
            " be the DataFrame returned by `emg_process()`."
        )

    # Determine what to display on the x-axis, mark activity.
    x_axis = np.linspace(
        0, emg_signals.shape[0] / info["sampling_rate"], emg_signals.shape[0]
    )
    emg_plot_static(id,type, emg_signals, x_axis, onsets, offsets, info["sampling_rate"])


def emg_preprocess_plot(id, emg_signals, sampling_rate):
    x_label = "Time (seconds)"
    x_axis = np.linspace(0, emg_signals.shape[0] / sampling_rate, emg_signals.shape[0])
    fig, ax0 = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))
    fig.suptitle("EMG's Preprocess Result--ID:" + id, fontweight="bold")
    # Plot cleaned and raw EMG.
    ax0.set_title("Raw and Cleaned Signal")
    ax0.plot(x_axis, emg_signals["EMG_Raw"], color="#B0BEC5", label="Raw", zorder=1)
    ax0.plot(
        x_axis,
        emg_signals["EMG_Clean"],
        color="#FFC107",
        label="Cleaned",
        zorder=1,
        linewidth=1.5,
    )
    ax0.set_xlabel(x_label)

    # Adjust layout
    plt.tight_layout()
    ax0.legend(loc="upper right")

def ppg_pre_plot(id,ppg_signals,info=None):
    fig, ax0 = plt.subplots(figsize=(8, 6))
    fig.suptitle("PPG--ID:" + id + "'s Preprocess Result", fontweight="bold")
    ax0 = _ppg_peaks_plot(
        ppg_signals["PPG_Clean"].values,
        info=info,
        sampling_rate=info["sampling_rate"],
        raw=ppg_signals["PPG_Raw"].values,
        ax=ax0,
    )

