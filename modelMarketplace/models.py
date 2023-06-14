import uuid
from django.db import models
from project.models import Project
from dataset.models import ProcessedDataset

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ModelSetup(BaseModel):
    MODEL_CHOICES = (
        ('classification', 'Classification'),
        ('detection', 'Object Detection'),
        ('segmentation', 'Image Segmentation')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='projectModel', blank=True)
    model_type = models.CharField(max_length=20, choices=MODEL_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Model Setup"


class ModelTrainingConfig(BaseModel):

    # CHOICES = (( WHAT GOES TO DB, WHAT USER SEES ))
    IMAGE_SIZE_CHOICES = (
        (224, "224x224"),
        (256, "256x256"),
        (416, "416x416"),
        (512, "512x512"),
        (640, "640x640"),
        (1024, "1024x1024"),
    )
    MODEL_CHOICE = (
        ("yolov5n", "YOLOv5 Nano"),
        ("yolov5s", "YOLOv5 Small"),
        ("yolov5m", "YOLOv5 Medium"),
        ("yolov5l", "YOLOv5 Large"),
        ("yolov5x", "YOLOv5 Extra-Large"),
    )
    BATCH_SIZE_CHOICE = (
        (16, 16),
        (32, 32),
        (64, 64),
        (128, 128),
    )
    OPTIMIZER_CHOICE = (
        ("SGD", "Stochastic Gradient Descent (SGD)"),
        ("Adam", "ADAM"),
        ("AdamW", "ADAM (Weight Decay)"),
    )
    model = models.ForeignKey(ModelSetup, on_delete=models.CASCADE, related_name='modelTraining')
    num_of_epochs = models.PositiveIntegerField(null=True, blank=True)
    img_size = models.PositiveIntegerField(choices=IMAGE_SIZE_CHOICES, default=640, null=True, blank=True)
    batch_size = models.PositiveIntegerField(choices=BATCH_SIZE_CHOICE, default=32, null=True, blank=True)
    yolo_choice = models.CharField(max_length=50, choices=MODEL_CHOICE, default="yolov5s", null=True, blank=True)
    optimizer = models.CharField(max_length=50, choices=OPTIMIZER_CHOICE, default="SGD", null=True, blank=True)

    def __str__(self):
        return "Training " + self.model.name

    class Meta:
        verbose_name_plural = "Model Training Config"


class ModelHistoryDetails(BaseModel):
    model = models.ForeignKey(ModelSetup, on_delete=models.CASCADE, related_name='modelHistory')
    train_accuracy = models.JSONField(null=True, blank=True)
    val_accuracy = models.JSONField(null=True, blank=True)
    train_loss = models.JSONField(null=True, blank=True)
    val_loss = models.JSONField(null=True, blank=True)
    classification_report = models.JSONField(null=True, blank=True)

    def __str__(self):
        return "History " + self.model.name

    class Meta:
        verbose_name_plural = "Model History Details"
