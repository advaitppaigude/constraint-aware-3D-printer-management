class PrintJob:
    """
    Reconstructed from the final NEA code listing.

    This is the scheduling-relevant portion of the original PrintJob class.
    School-specific priority behaviour is retained here for reference only.
    """

    def __init__(
        self,
        creator,
        filename,
        colourPreference,
        materialPreference,
        NEA=False,
        clientSideReconstruction=False,
    ):
        self.creator = creator

        if clientSideReconstruction:
            self.filename = filename
            self.f = 0.0
            self.t = 0
            self.layerHeight = 0.0
            self.x = 0.0
            self.y = 0.0
            self.z = 0.0
            self.quality = ""
            self.density = ""
        else:
            self.filename = creator + filename

            with open(self.filename + ".gcode", "r") as file:
                line = file.read().split("\n")

            self.t = int(line[1].split(":")[1].strip())
            self.f = float(line[2].split(":")[1].strip()[:-1])
            self.layerHeight = float(line[3].split(":")[1].strip())

            self.x = (
                float(line[7].split(":")[1].strip())
                - float(line[4].split(":")[1].strip())
            )
            self.y = (
                float(line[8].split(":")[1].strip())
                - float(line[5].split(":")[1].strip())
            )
            self.z = (
                float(line[9].split(":")[1].strip())
                - float(line[6].split(":")[1].strip())
            )
            self.dimensions = [self.x, self.y, self.z]

            self.quality = "Unknown"
            self.density = "Unknown"

            for c in range(len(line) - 5, len(line) - 1):
                if "quality_type" in line[c]:
                    self.quality = (
                        line[c]
                        .split("quality_type = ")[1]
                        .split("\\")[0]
                        .strip()
                    )
                elif "sparse_density" in line[c]:
                    self.density = (
                        line[c]
                        .split("sparse_density = ")[1]
                        .split("\\")[0]
                        .strip()
                    )

        self.colourPreference = colourPreference
        self.materialPreference = materialPreference
        self.studentComment = ""
        self.teacherComment = ""
        self.isNEA = NEA

        if self.isNEA:
            self.p = 3600
        else:
            self.p = 0

    def RecalculatePriority(self, t):
        self.p += t
        if self.isNEA:
            self.p += t * 0.5

    def ToDict(self):
        return {
            "Creator": self.creator,
            "Filename": self.filename,
            "Duration": self.t,
            "Filament": self.f,
            "X": self.x,
            "Y": self.y,
            "Z": self.z,
            "ColourPreference": self.colourPreference,
            "MaterialPreference": self.materialPreference,
            "Quality": self.quality,
            "LayerHeight": self.layerHeight,
            "Density": self.density,
            "StudentComment": self.studentComment,
            "TeacherComment": self.teacherComment,
            "IsNEA": self.isNEA,
        }
