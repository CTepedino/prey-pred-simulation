package ar.edu.itba.ss.model;

public record Vector2D(double x, double y) {

    public static Vector2D zero(){
        return new Vector2D(0, 0);
    }

    public static Vector2D fromPolar(double magnitude, double angle){
        return new Vector2D(magnitude * Math.cos(angle), magnitude * Math.sin(angle));
    }

    public Vector2D add(Vector2D v){
        return new Vector2D(x + v.x, y + v.y);
    }

    public Vector2D subtract(Vector2D v){
        return new Vector2D(x - v.x, y - v.y);
    }

    public Vector2D scale(double k){
        return new Vector2D(k*x, k*y);
    }

    public double dot(Vector2D v){
        return x * v.x + y * v.y;
    }

    public double cross(Vector2D v){
        return this.x * v.y - this.y * v.x;
    }

    public double magnitude(){
        return Math.hypot(x, y);
    }

    public Vector2D normalize(){
        double mag = magnitude();
        if (mag == 0) return zero();
        return new Vector2D(x/mag, y/mag);
    }

    public double distanceTo(Vector2D v){
        return this.subtract(v).magnitude();
    }

    public double distanceSq(Vector2D v){
        double dx = x - v.x;
        double dy = y - v.y;
        return dx*dx + dy*dy;
    }


    public Vector2D rotate(double angle) {
        double cos = Math.cos(angle);
        double sin = Math.sin(angle);
        return new Vector2D(cos * x - sin * y, sin * x + cos * y);
    }

    public Vector2D perpendicular(){
        return new Vector2D(-y, x);
    }

    public double angleWith(Vector2D v) {
        double dot = this.dot(v);
        double mags = this.magnitude() * v.magnitude();
        if (mags == 0) return 0;
        double cos = dot / mags;
        return Math.acos(Math.max(-1.0, Math.min(1.0, cos))); // evita NaN por redondeo
    }

    public double signedAngleTo(Vector2D other) {
        double dot = this.dot(other);
        double det = this.x * other.y - this.y * other.x; // determinante 2D
        return Math.atan2(det, dot); // valor en [-π, π]
    }

    public Vector2D projectOnto(Vector2D v) {
        double scale = this.dot(v) / v.dot(v);
        return v.scale(scale);
    }

}
