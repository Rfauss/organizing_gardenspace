from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import user, garden


@app.route("/gardens")
def displayGarden():
    if "user_id" not in session:
        return redirect("/")
    else:
        localGarden = garden.Garden.getGarden({"user_id": session["user_id"]})
        if localGarden == False:
            return render_template(
                "garden/garden.html",
                current_user=user.User.getById({"id": session["user_id"]}),
                garden=[],
                all_containers=[],
            )
        else:
            session["garden_id"] = localGarden[0]["id"]
            rowCount = int(localGarden[0]["rows"])
            colCount = int(localGarden[0]["columns"])
            totalCount = rowCount * colCount
            containerCount = 1
            listContainers = (
                garden.Garden.getContainers({"id": localGarden[0]["id"]}),
            )
            all_containers = {}
            for eachDictionary in listContainers[0]:
                if containerCount > totalCount:
                    containerCount = 1
                    break
                all_containers.update({containerCount: eachDictionary})
                containerCount += 1

            return render_template(
                "garden/garden.html",
                garden=localGarden,
                rowCount=rowCount,
                colCount=colCount,
                all_containers=all_containers,
                totalCount=totalCount,
            )


@app.route("/gardens/warning")
def warnGarden():
    if "user_id" not in session:
        return redirect("/")
    else:
        return render_template("garden/gardenWarning.html")


@app.route("/gardens/delete")
def deleteGarden():
    if "user_id" not in session:
        return redirect("/")
    else:
        if "garden_id" not in session:
            return redirect("/gardens")
        else:
            all_containers = garden.Garden.getContainers({"id": session["garden_id"]})
            for eachContainer in all_containers:
                garden.Garden.deletePlants({"id": eachContainer["id"]})
            garden.Garden.deleteAllContainers({"id": session["garden_id"]})
            garden.Garden.deleteGarden({"id": session["user_id"]})
            session.pop("garden_id", default=None)
            return redirect("/gardens")


@app.route("/gardens/create")
def createGarden():
    if "user_id" not in session:
        return redirect("/")
    return render_template(
        "garden/gardenCreate.html",
        current_user=user.User.getById({"id": session["user_id"]}),
    )


@app.route("/gardens/add", methods=["POST"])
def addGarden():
    if "user_id" not in session:
        return redirect("/")
    if garden.Garden.validate_create(request.form):
        location = int(request.form["location"])
        user_id = session["user_id"]
        data = {
            "garden_name": request.form["garden_name"],
            "location": location,
            "rows": int(request.form["rows"]),
            "columns": int(request.form["columns"]),
            "user_id": user_id,
        }
        garden.Garden.save(data)
        return redirect("/gardens")
    return redirect("/gardens")


@app.route("/plots/edit/<int:id>")
def editPlot(id):
    if "user_id" not in session:
        return redirect("/")
    container_contents = garden.Garden.getPlants({"container_id": id})
    print(f"Container contents are: {container_contents}")
    if container_contents == False:
        container_contents = []
        session["container_id"] = id
        return render_template(
            "garden/gardenUpdate.html",
            container_contents=container_contents,
        )
    else:
        session["container_id"] = id
        session["plant_id"] = container_contents[0]["id"]
        return render_template(
            "garden/gardenUpdate.html",
            container_contents=container_contents,
        )


@app.route("/plots/add", methods=["POST"])
def addPlants():
    if "user_id" not in session:
        return redirect("/")
    if garden.Garden.validate_plants(request.form):
        data = {
            "name": request.form["plant_name"],
            "count": request.form["plant_count"],
            "container_id": session["container_id"],
        }
        if request.form.get("check_plant_delete") == "checked":
            garden.Garden.deletePlantsById({"plant_id": session["plant_id"]})
            return redirect("/gardens")
        if request.form["plant_id"] == "Null":
            garden.Garden.insertIntoContainers(data)
            session.pop("container_id")
            return redirect("/gardens")
        else:
            data = {
                "name": request.form["plant_name"],
                "count": request.form["plant_count"],
                "container_id": session["container_id"],
                "plant_id": session["plant_id"],
            }
            garden.Garden.updateContainer(data)
            session.pop("container_id")
            session.pop("plant_id")
            return redirect("/gardens")
    else:
        return redirect("/gardens")
