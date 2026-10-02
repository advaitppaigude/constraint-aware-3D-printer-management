from datetime import datetime


class Optimiser:
    def ChooseBestJob(self, printer):
        now = datetime.now()
        currentTimeInSeconds = (
            now.hour * 3600 + now.minute * 60 + now.second
        )
        timeTillEndOfSchoolDay = 16 * 3600 - currentTimeInSeconds

        feasibleRegion = {
            "t": timeTillEndOfSchoolDay,
            "f": printer.remainingLength,
        }

        currentBestJob = 0
        currentBestProfitSacrificeVal = float("-inf")

        for index, currentJob in enumerate(printer.jobPool):
            feasibleRegionAfterConsideration = {
                "t": feasibleRegion["t"] - currentJob.t,
                "f": feasibleRegion["f"] - currentJob.f,
            }

            sacrifice = 0

            for i, job in enumerate(printer.jobPool):
                if (
                    job.t > feasibleRegionAfterConsideration["t"]
                    or job.f > feasibleRegionAfterConsideration["f"]
                ):
                    if i != index:
                        sacrifice += job.p

            currentProfitSacrificeVal = currentJob.p - sacrifice

            if currentProfitSacrificeVal > currentBestProfitSacrificeVal:
                currentBestProfitSacrificeVal = currentProfitSacrificeVal
                currentBestJob = index

        return printer.jobPool[currentBestJob]
