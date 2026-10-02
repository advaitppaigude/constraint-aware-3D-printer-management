# Reconstructed from the final server-side scheduling code.
# This retains the original school-specific logic for reference.

import time

waitingRoom = []


def CurrentTimeInSeconds():
    t = time.localtime()
    return (t.tm_hour * 3600) + (t.tm_min * 60) + t.tm_sec


def UpdateJobPriorities(timeAtPreviousUpdate):
    currentTime = CurrentTimeInSeconds()
    interval = currentTime - timeAtPreviousUpdate

    for job in waitingRoom:
        job.RecalculatePriority(interval)

    return currentTime


def PopulateJobPool(printer):
    global waitingRoom

    for job in waitingRoom[:]:
        # Original system only considered jobs which could finish before 16:00
        # and which fit within the printer's remaining filament.
        if (
            job.t < (16 * 3600 - CurrentTimeInSeconds())
            and job.f < printer.remainingLength
        ):
            if (
                job.colourPreference["Fixed"]
                and job.materialPreference["Fixed"]
            ):
                if (
                    job.colourPreference["Colour"] == printer.colour
                    and job.materialPreference["Type"] == printer.type
                ):
                    printer.jobPool.append(job)
                    waitingRoom.remove(job)

            elif job.colourPreference["Fixed"]:
                if job.colourPreference["Colour"] == printer.colour:
                    printer.jobPool.append(job)
                    waitingRoom.remove(job)

            elif job.materialPreference["Fixed"]:
                if job.materialPreference["Type"] == printer.type:
                    printer.jobPool.append(job)
                    waitingRoom.remove(job)

            else:
                if job.p < 28800:
                    # For the first school day, honour both non-fixed
                    # preferences where possible.
                    if (
                        job.colourPreference["Colour"] == printer.colour
                        and job.materialPreference["Type"] == printer.type
                    ):
                        printer.jobPool.append(job)
                        waitingRoom.remove(job)
                else:
                    # After one school day, allow any feasible printer.
                    printer.jobPool.append(job)
                    waitingRoom.remove(job)
